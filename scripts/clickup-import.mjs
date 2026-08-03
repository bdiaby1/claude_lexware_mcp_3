#!/usr/bin/env node
// Creates one Lexware Office bookkeeping voucher (purchaseinvoice) per ClickUp
// receipt in scripts/clickup-manifest.json, categorized under a posting
// category you choose, and attaches the matching PDF.
//
// Run where api.lexware.io is reachable (not inside a network-restricted
// Claude Code sandbox). Requires LEXWARE_OFFICE_API_KEY, e.g.:
//   node --env-file=.env scripts/clickup-import.mjs --list-categories
//   node --env-file=.env scripts/clickup-import.mjs --category-id <uuid> --receipts ./clickup-receipts
//   node --env-file=.env scripts/clickup-import.mjs --category-id <uuid> --receipts ./clickup-receipts --yes

import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BASE_URL = process.env.LEXWARE_OFFICE_API_BASE_URL ?? 'https://api.lexware.io';
const API_KEY = process.env.LEXWARE_OFFICE_API_KEY;

function parseArgs(argv) {
	const args = { receipts: './clickup-receipts', yes: false, listCategories: false };
	for (let i = 0; i < argv.length; i++) {
		const a = argv[i];
		if (a === '--receipts') args.receipts = argv[++i];
		else if (a === '--category-id') args.categoryId = argv[++i];
		else if (a === '--contact-id') args.contactId = argv[++i];
		else if (a === '--yes') args.yes = true;
		else if (a === '--list-categories') args.listCategories = true;
		else throw new Error(`Unknown argument: ${a}`);
	}
	return args;
}

async function lexFetch(pathname, options = {}) {
	const res = await fetch(`${BASE_URL}${pathname}`, {
		...options,
		headers: {
			Authorization: `Bearer ${API_KEY}`,
			Accept: 'application/json',
			...(options.body && !(options.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}),
			...options.headers,
		},
	});
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`${options.method ?? 'GET'} ${pathname} -> HTTP ${res.status}: ${text}`);
	}
	return res.status === 204 ? null : res.json();
}

async function listPostingCategories() {
	const categories = await lexFetch('/v1/posting-categories');
	const all = Array.isArray(categories) ? categories : (categories.content ?? []);
	const candidates = all.filter((c) => /lizenz/i.test(c.name ?? ''));
	console.log(`Found ${all.length} posting categories, ${candidates.length} matching "Lizenz*":\n`);
	for (const c of candidates.length ? candidates : all) {
		console.log(`  ${c.id}  ${c.name}`);
	}
	if (!candidates.length) {
		console.log('\nNo "Lizenzen"-named category found — inspect the full list above and pick the closest match manually.');
	}
	return candidates;
}

async function findClickUpContact() {
	const result = await lexFetch('/v1/contacts?name=ClickUp');
	const matches = result?.content ?? [];
	return matches.length === 1 ? matches[0].id : undefined;
}

async function main() {
	const args = parseArgs(process.argv.slice(2));

	if (!API_KEY) {
		console.error('LEXWARE_OFFICE_API_KEY is not set. Run with: node --env-file=.env scripts/clickup-import.mjs ...');
		process.exit(1);
	}

	if (args.listCategories) {
		await listPostingCategories();
		return;
	}

	if (!args.categoryId) {
		console.error('Missing --category-id. Run with --list-categories first to find the "Lizenzen und Konzessionen" category id in your chart of accounts.');
		process.exit(1);
	}

	const manifestPath = path.join(__dirname, 'clickup-manifest.json');
	const { entries } = JSON.parse(await readFile(manifestPath, 'utf8'));

	let contactId = args.contactId;
	if (!contactId && args.yes) {
		contactId = await findClickUpContact().catch(() => undefined);
		if (contactId) console.log(`Using existing ClickUp contact: ${contactId}`);
	}

	console.log(args.yes ? 'LIVE RUN — creating vouchers in Lexware Office.\n' : 'DRY RUN (pass --yes to actually create vouchers).\n');

	let total = 0;
	const results = [];

	for (const entry of entries) {
		const filePath = path.resolve(args.receipts, entry.file);
		const fileExists = existsSync(filePath);
		total += entry.bankAmountEur;

		const voucherBody = {
			type: 'purchaseinvoice',
			voucherDate: entry.voucherDate,
			totalGrossAmount: entry.bankAmountEur,
			totalTaxAmount: 0,
			taxType: 'gross',
			...(contactId ? { contactId } : {}),
			remark: `ClickUp – ${entry.plan} (${entry.reference})`,
			voucherItems: [
				{ amount: entry.bankAmountEur, taxAmount: 0, taxRatePercent: 0, categoryId: args.categoryId },
			],
		};

		if (!fileExists) {
			console.warn(`SKIP ${entry.file}: not found under ${args.receipts}`);
			results.push({ ...entry, status: 'missing-file' });
			continue;
		}

		if (!args.yes) {
			console.log(`[dry-run] ${entry.voucherDate}  ${entry.bankAmountEur.toFixed(2)} EUR  ${entry.file}  (${entry.plan})`);
			results.push({ ...entry, status: 'dry-run' });
			continue;
		}

		try {
			const voucher = await lexFetch('/v1/vouchers', { method: 'POST', body: JSON.stringify(voucherBody) });
			const fileBuffer = await readFile(filePath);
			const form = new FormData();
			form.append('file', new Blob([fileBuffer], { type: 'application/pdf' }), entry.file);
			await lexFetch(`/v1/vouchers/${voucher.id}/files`, { method: 'POST', body: form });
			console.log(`OK    ${entry.voucherDate}  ${entry.bankAmountEur.toFixed(2)} EUR  voucher ${voucher.id}  (${entry.file})`);
			results.push({ ...entry, status: 'created', voucherId: voucher.id });
		} catch (err) {
			console.error(`FAIL  ${entry.file}: ${err.message}`);
			results.push({ ...entry, status: 'error', error: err.message });
		}
	}

	console.log(`\nTotal: ${total.toFixed(2)} EUR across ${entries.length} receipts.`);
	if (!args.yes) {
		console.log('Review the plan above, then re-run with --yes to create the vouchers and attach the PDFs.');
	}
	const failed = results.filter((r) => r.status === 'error' || r.status === 'missing-file');
	if (failed.length) process.exitCode = 1;
}

main().catch((err) => {
	console.error(err);
	process.exit(1);
});
