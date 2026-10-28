# Clarity — Investment Studio

A dependency-free, responsive investment conversation simulator. Open `dist/index.html` directly or serve `dist/` with any static web server.

## Features
Seven tabs cover overview, needs, editable example products, maturity scenarios, historical replay, suitability comparison, and decision records. Client inputs and immutable decision snapshots are saved in browser localStorage. Reports download as text; browser print supports PDF.

## Model
- Note: principal × [1 + max(floor − 1, min(cap, total market return × participation))] − fee.
- Deposit: principal × (1 + rate)^term − fee.
- Market: max(0, principal × (1 + total market return) − fee).
- Fee is a one-time percentage of original principal at maturity. Taxes, issuer default, and interim product valuation are excluded.
- Suitability checks maturity timing, worst contractual capital loss, liquidity, and target feasibility. A pass is not a recommendation or guaranteed target achievement.
- Historical data: Nifty 50 TR annual returns, 2000–2022, rounded to one decimal, from NSE Indices’ Nifty 50 at 20,000 report (linked in app). Replay compounds annual data and applies the current product formula at maturity. No daily drawdown analysis.

## Scope
This is a functional demonstration, not a bank production system. It has no bank integration, live market feed, cloud customer database, compliance certification, or real product execution. Device storage can be cleared; export decisions to retain them. Example client data is fictional.

## Source
- dist/index.html: shell
- dist/style.css: responsive layout
- dist/engine.js: shared financial and suitability engine
- dist/app.js: navigation, forms, charts and reports

## Client dashboard
Open `#client-view` or choose **Client dashboard** in the manager workspace. The client view includes My goal, My options, My decision, and My reports. It consumes the same saved manager inputs and formulas. Preferences are saved separately from manager decisions and shown in the RM review; changed inputs mark prior preferences as requiring reconfirmation. Same-origin browser tabs sync via storage events. Client summaries download as plain text.

This is a same-browser handoff, not independent customer authentication or cross-device synchronization. The view switch is navigation, not an access-control boundary. The published site remains owner-private. A separate multi-user deployment needs authenticated client accounts and server-side records.

## Dynamic mathematical scenarios
Scenarios now includes an independent live calculator, seeded from the saved plan. Enter principal, whole-year tenure and annual interest, or switch to target-profit mode to solve the required annual rate. Simple interest and compound interest (annual, quarterly, monthly) are supported. The time graph, profit, maturity balance, formula and yearly table update immediately. A year slider inspects intermediate balances. Invalid fields hide stale results. Monthly/quarterly rates are nominal annual rates. No fees, taxes, inflation, deposits or withdrawals are included in this educational calculator.

Calculator exploration does not modify the client plan. Existing market-product scenarios remain below it, using the saved plan and live payout markers. The client dashboard links to the calculator.

Run checks with `node tests/math.test.cjs` and `node tests/client.test.cjs`.
