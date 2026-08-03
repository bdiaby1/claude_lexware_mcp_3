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
	for (let attempt = 0; ; attempt++) {
		const res = await fetch(`${BASE_URL}${pathname}`, {
			...options,
			headers: {
				Authorization: `Bearer ${API_KEY}`,
				Accept: 'application/json',
				...(options.body && !(options.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}),
				...options.headers,
			},
		});
		if (res.status === 429 && attempt < 5) {
			await new Promise((r) => setTimeout(r, 1000 * (attempt + 1)));
			continue;
		}
		if (!res.ok) {
			const text = await res.text().catch(() => '');
			throw new Error(`${options.method ?? 'GET'} ${pathname} -> HTTP ${res.status}: ${text}`);
		}
		return res.status === 204 ? null : res.json();
	}
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

async function resolveCategoryId(explicitId) {
	if (explicitId) return explicitId;
	const categories = await lexFetch('/v1/posting-categories');
	const all = Array.isArray(categories) ? categories : (categories.content ?? []);
	const candidates = all.filter((c) => /lizenz/i.test(c.name ?? ''));
	// Prefer the plain, non-automatic category over §13b/§13b Drittland variants:
	// those require a real 19% self-assessment tax rate (API rejects 0%), which
	// needs deliberate reverse-charge tax handling, not a default guess.
	const plain = candidates.find((c) => (c.name ?? '').trim() === 'Lizenzen und Konzessionen');
	if (plain) {
		console.log(`Auto-selected posting category: ${plain.id}  (${plain.name})\n`);
		return plain.id;
	}
	if (candidates.length === 1) {
		console.log(`Auto-selected posting category: ${candidates[0].id}  (${candidates[0].name})\n`);
		return candidates[0].id;
	}
	if (candidates.length === 0) {
		console.error('No posting category matching "Lizenz*" found in your chart of accounts. Run --list-categories to see all categories, then pass --category-id explicitly.');
	} else {
		console.error(`${candidates.length} posting categories match "Lizenz*" — ambiguous, pass --category-id explicitly:`);
		for (const c of candidates) console.error(`  ${c.id}  ${c.name}`);
	}
	process.exit(1);
}

async function findOrCreateClickUpContact() {
	for (const name of ['Mango Technologies', 'ClickUp']) {
		const result = await lexFetch(`/v1/contacts?name=${encodeURIComponent(name)}`);
		const matches = result?.content ?? [];
		if (matches.length === 1) return matches[0].id;
	}
	const created = await lexFetch('/v1/contacts', {
		method: 'POST',
		body: JSON.stringify({
			version: 0,
			roles: { vendor: {} },
			company: { name: 'Mango Technologies Inc DBA ClickUp' },
			addresses: { billing: [{ street: '350 Tenth Ave, Suite 500', city: 'San Diego', zip: '92101', countryCode: 'US' }] },
		}),
	});
	console.log(`Created vendor contact for Mango Technologies Inc DBA ClickUp: ${created.id}`);
	return created.id;
}

async function findExistingVoucher(voucherNumber) {
	const result = await lexFetch(`/v1/vouchers?voucherNumber=${encodeURIComponent(voucherNumber)}`);
	const matches = result?.content ?? [];
	return matches.find((v) => v.voucherNumber === voucherNumber);
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

	const categoryId = await resolveCategoryId(args.categoryId);

	const manifestPath = path.join(__dirname, 'clickup-manifest.json');
	const { entries } = JSON.parse(await readFile(manifestPath, 'utf8'));

	let contactId = args.contactId;
	if (!contactId && args.yes) {
		contactId = await findOrCreateClickUpContact();
		console.log(`Using vendor contact: ${contactId}`);
	}

	console.log(args.yes ? 'LIVE RUN — creating vouchers in Lexware Office.\n' : 'DRY RUN (pass --yes to actually create vouchers).\n');

	let total = 0;
	const results = [];

	for (const entry of entries) {
		const filePath = path.resolve(args.receipts, entry.file);
		const fileExists = existsSync(filePath);
		const voucherNumber = entry.file.replace(/\.pdf$/i, '');
		total += entry.bankAmountEur;

		const voucherBody = {
			type: 'purchaseinvoice',
			voucherNumber,
			voucherDate: entry.voucherDate,
			totalGrossAmount: entry.bankAmountEur,
			totalTaxAmount: 0,
			taxType: 'gross',
			...(contactId ? { contactId } : {}),
			remark: `ClickUp – ${entry.plan} (${entry.reference})`,
			voucherItems: [
				{ amount: entry.bankAmountEur, taxAmount: 0, taxRatePercent: 0, categoryId },
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

		await new Promise((r) => setTimeout(r, 700)); // stay under the Lexware API rate limit
		let existing;
		try {
			existing = await findExistingVoucher(voucherNumber);
		} catch (err) {
			console.error(`FAIL  ${entry.file}: could not verify existing voucher (${err.message}) — skipping to avoid a duplicate`);
			results.push({ ...entry, status: 'error', error: err.message });
			continue;
		}
		if (existing) {
			console.log(`SKIP  ${entry.voucherDate}  ${voucherNumber} already booked as voucher ${existing.id}`);
			results.push({ ...entry, status: 'already-exists', voucherId: existing.id });
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
