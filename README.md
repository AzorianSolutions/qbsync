# QBSync by [Azorian Solutions](https://azorian.solutions)

This application provides the ability to export data from Quickbooks Desktop into various formats and databases.

At this time, you may only export to JSON and YAML format but future support is planned for CSV as well as
direct injection into MySQL, PgSQL, and SQLite databases.

This project took hints from Sroeurnsuon's [pyQBWC fork](https://github.com/Sroeurnsuon/pyQBWC) of
BillBarry's original [pyqwc project](https://github.com/BillBarry/pyqwc/tree/master/pyqwc). I didn't have much time to
get up to speed on the QBWC implementation, so I studied Sroeurnsuon's implementation and then re-built it with better
abstraction, organization, and security.

I only had two days to get this completed in its entirety, so I will provide
more updates in the future. I would certainly love for anyone interested in contributing or maintaining the project to
contact me.

## Quick reference

- **Maintained by:** [Matt Scott](https://github.com/AzorianSolutions)
- **Website:** [https://azorian.solutions](https://azorian.solutions)
- **Current Version:** 0.1.0
- **Github:** [https://github.com/AzorianSolutions/qbsync](https://github.com/AzorianSolutions/as-apps-qbsync)

## TL;DR

    git clone https://github.com/AzorianSolutions/qbsync.git
    cd qbsync
    python ./run.py

## Deploying this application

Check out [this tutorial](doc/tutorial.md) for information on deploying and operating this application.
