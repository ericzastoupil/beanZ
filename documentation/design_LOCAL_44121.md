# Design Documentation for beanZ

## Purpose
This application is intended to enable and inform a user's financial decision-making by providing a comprehensive financial snapshot and analysis of a their financial health and habits. It might also just be an excuse for me to practice by building something.

## Features
- [ ] User Registration
    - [ ] User profiles- username, pic, email
- [ ] Log-in
    - [ ] Secure authentication
- [ ] Splash screen
    - [ ] Some kind of logo/imagery/branding
- [ ] Navigation bar
- [ ] Track spending
    - [ ] By category and subcategory. 4 main categories: Income, Expenses, Assets, Liabilities
    - [ ] By date
- [ ] Ingest financial documents and translate them into database records.
    - [ ] Pay stubs
    - [ ] Bank transactions
    - [ ] Investment transactions
- [ ] Current monthly spending by category
- [ ] Account and Networth progression over time
- [ ] Drag and drop transaction documents for ingest
- [ ] Hosted and accessible on LAN, containerized

## User Interface
1. Provide historical averages of spending by category and sub category. (sankey diagram?)

2. Display current spending
    - By category
    - Compared to previous spending averages

## Incoroporated Technologies
| Tech | Description of Use |
| ----------- | ----------- |
| Flask  | Framework Stuff and things |
| Python | More stuff and things |
| SQLite | Db stuff and things |
| Apache | Web stuff |
| Docker | Container stuffs |

## Branch Strategy (implemented)
- Main- Always maintains a production-ready state
- Develop- Delivery of most recently developed features, preparing for next release. When stable and ready for release, merges back into Main.
- Feature- Branches off of, and merges back into, develop branch.

## Long term goals
- Host in the cloud to be accessible through www
- Built in budgeting
- Connect through financial aggregator (Plaid) to automate ingest
- Apply predictive tagging recommendations