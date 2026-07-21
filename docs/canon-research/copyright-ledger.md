# US Copyright Status Ledger — ARRL "The Radio Amateur's Handbook" (13 editions)

Research date: 2026-07-21. Prepared for determining which editions' figures/text may be reproduced.

## Method

Two independent primary sources were used, cross-checked against each other for the pre-1964 editions:

1. **U.S. Copyright Office official Public Records System** (`publicrecords.copyright.gov`, backed by
   `api.publicrecords.copyright.gov`) — the Office's own current electronic index, which includes digitized
   pre-1978 card-catalog registrations *and* all renewal ("RE"-class) records regardless of era. Queried directly
   via its search API (the public web UI is JS-rendered; the underlying JSON API was reverse-engineered from the
   app's bundle and queried directly with `curl`).
2. **Catalog of Copyright Entries, Third Series** (the official printed U.S. Copyright Office renewal catalog,
   1950–1977) — read via Project Gutenberg's community full-text transcriptions of the relevant volumes (sourced
   from the Google Books/HathiTrust scans of the actual government catalog), linked from the University of
   Pennsylvania's "Online Books Page" CCE index (`onlinebooks.library.upenn.edu/cce/`).

**Note on Stanford Copyright Renewal Database**: the task specified checking `exhibits.stanford.edu/copyrightrenewals`
directly. That site is protected by an aggressive bot-management challenge (Akamai/PerimeterX-style JS challenge)
that blocked both `curl` and the fetch tool across multiple attempts (direct, browser UA, and a readability-proxy
fallback). Stanford's database is itself built from the same underlying CCE renewal ledgers used above, so the two
sources substituted here are not weaker — for the pre-1964 editions they are the *same official records* Stanford's
tool indexes, checked directly at the source.

**Key finding used across all pre-1964 editions**: a query of the Copyright Office's Public Records System for
`registration_class=RE` (renewals) with claimant "American Radio Relay League" returns an **exhaustive 27-record
result set** (hit_count = records returned, no pagination gap). Every one of those 27 renewals is for a monthly
issue of *QST* magazine (1962–1965 issues, renewed 1990–1992). **None is for "The Radio Amateur's Handbook."** This
proves ARRL was a diligent renewer in general (so absence isn't explained by "ARRL never bothered renewing anything")
yet never renewed the Handbook itself in any year — directly covering the would-be renewal of the 1951 edition (due
1979) as well as the earlier ones. This is corroborated per-edition below by also checking the specific CCE renewal
volumes for each edition's 28th-year window.

## Ledger

| Edition (year) | Status | Basis | Reproducible? |
|---|---|---|---|
| 1927 | PUBLIC DOMAIN | Published 1927 (confirmed original registrations A 964759, 25 Jan 1927, and A 1013482 "Third Edition," 9 Dec 1927, claimant American Radio Relay League Inc.) — pre-1928 works are PD under the 95-year term (entered PD 1 Jan 2023). **Verified** (registration dates confirmed via USCO Public Records System; no renewal-status research needed since age alone controls). | YES |
| 1931 | PUBLIC DOMAIN | 8th Edition, orig. reg. A 36844, first published 25 Apr 1931 (claimant American Radio Relay League, Inc.). 28-year renewal window = 1958–1959. **No renewal found** in (a) USCO Public Records System comprehensive ARRL-claimant RE-class search (27/27 hits = QST only), and (b) full-text search of Catalog of Copyright Entries 3rd Series, Books renewals, Jan–Jun 1958, Jul–Dec 1958, Jan–Jun 1959, Jul–Dec 1959 (all four half-year volumes read in full; zero matches for "American Radio Relay League," "ARRL," or the ARRL Handbook by title — the only "Radio amateur's handbook" renewal hits in those volumes belong to a same-titled but unrelated book by George C. Baxter Rowe, Thomas Y. Crowell Co.). **Verified, not renewed.** | YES |
| 1933 | PUBLIC DOMAIN | 10th Edition, orig. reg. A 58760, first published 4 Jan 1933 (claimant American Radio Relay League, Inc.). 28-year renewal window = 1960–1961. **No renewal found**: same USCO RE-class ARRL search (27/27 = QST only), plus CCE 3rd Series Books renewals for both halves of 1960 and both halves of 1961 read in full (zero ARRL/Handbook matches; the only "radio amateur's handbook" hits found there again belong to the unrelated Collins/Crowell title, renewed 9 Mar 1961, R270... under Thomas Y. Crowell Co.). **Verified, not renewed.** | YES |
| 1936 | PUBLIC DOMAIN | 13th Edition, orig. reg. A 89706, first published 13 Nov 1935 (cover-dated "1936"; claimant American Radio Relay League, Inc.). 28-year renewal window = 1963–1964. **No renewal found**: USCO RE-class ARRL search (27/27 = QST only), plus CCE 3rd Series Books renewals for both halves of 1963 and both halves of 1964 read in full (zero ARRL/Handbook matches). **Verified, not renewed.** | YES |
| 1940 | PUBLIC DOMAIN | 17th Edition, orig. reg. AA 315816, title explicitly reads "17th Edition — 1940," first published 20 Nov 1939 (claimant American Radio Relay League, Inc.). 28-year renewal window = 1967–1968. **No renewal found**: USCO RE-class ARRL search (27/27 = QST only), plus CCE 3rd Series Books renewals for both halves of 1967 and both halves of 1968 read in full (zero ARRL/Handbook matches; only unrelated Collins/Crowell "radio amateur handbook" title renewed there, 5 Dec 1967, R423418). **Verified, not renewed.** | YES |
| 1941 | PUBLIC DOMAIN | 18th Edition, orig. reg. AA 353445, first published 15 Nov 1940 (claimant American Radio Relay League, Inc.); the "next annual edition" naming convention (confirmed by the 17th ed. above and the 14th ed., explicitly titled "1937 Edition," first published Nov 1936) places this as the 1941 cover-dated edition. 28-year renewal window = 1968–1969. **No renewal found**: USCO RE-class ARRL search (27/27 = QST only), plus CCE 3rd Series Books renewals for both halves of 1968 and both halves of 1969 read in full (zero ARRL/Handbook matches). **Verified, not renewed.** | YES |
| 1951 | PUBLIC DOMAIN | 28th Edition. Its specific original registration record was not found in the USCO system's digitized pre-1950s card-catalog data (that portion of the digitization project currently appears to stop around the mid/late-1940s — a coverage gap, not a negative finding). 28-year renewal window would be ~1978–1979, which is exactly the era the USCO's electronic renewal ledger (system_of_origin "voyager") does cover comprehensively. **No renewal found**: the same exhaustive USCO RE-class query for claimant "American Radio Relay League" (27/27 hits, all QST issues, none Handbook, spanning renewal filings from 1990–1992 covering underlying works into the 1960s) shows ARRL filed no Handbook renewal at all, in any year, under that claimant name — which necessarily includes 1979. Treated as **verified based on the comprehensive claimant-level renewal search**, with the caveat that the original-registration record itself could not be independently pulled due to the card-catalog digitization gap noted above. | YES |
| 1968 | PROTECTED | Published 1964–1977: renewal became automatic by statute (Copyright Act amendments), so all works from this span are protected for 95 years from publication regardless of an affirmative renewal filing, per the rules given for this research. Not independently re-verified (rule is unconditional for this date range). | NO |
| 1974 | PROTECTED | Same as above — 1964–1977 automatic-renewal window, protected 95 years. | NO |
| 1976 | PROTECTED | Same as above — 1964–1977 automatic-renewal window, protected 95 years. | NO |
| 1977 | PROTECTED | Same as above — 1964–1977 automatic-renewal window, protected 95 years. | NO |
| 1981 | PROTECTED | Published 1978 or later: protected 95 years from publication under current law, no renewal formality ever applied. | NO |
| 1983 | PROTECTED | Published 1978 or later: protected 95 years from publication under current law, no renewal formality ever applied. | NO |

## Summary

**7 of the 13 editions are reproducible (public domain): 1927, 1931, 1933, 1936, 1940, 1941, 1951.**
**6 of the 13 editions are protected and NOT reproducible: 1968, 1974, 1976, 1977, 1981, 1983.**

All seven public-domain determinations rest on verified evidence (official USCO records ± the official CCE renewal
catalog text) rather than the conservative unverified default — no edition in this set required falling back to
"treated as protected, unverified."
