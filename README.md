# Bid Evaluation App

Evaluate and Score Bids in Odoo

## Overview

This app extends the functionality of the 'Purchase Agreements' workflow within Odoo allowing you to evaluate individual bids recieved as part of a tender or a purchase agreement. You can create bid evaluation templates and define checklists and scoring questions and use the templates to conduct the evaluations. An accompanying module enables the use of purchase panels for the evaluation process. Link to the app on the Odoo app store: (To be added once published)

## How To Use

To evaluate bids:

1. Once the app is installed, enable bids evaluation from your desired purchase agreements type under Purchase -> Configuration.
2. Create an evaluation template from Purchase -> Configuration -> Evaluation Template.
3. Select the evaluation template from within the purchase agreement record you have created.
4. Generate an evaluation record for each quotation and fill in the evaluation and validate the evaluation record.
5. Use the number of reports available for documenting the evaluation if required.

To enable use of purchase panels:

1. Check the 'Enable Purchase Panels' option from Purchase -> Settings
2. Create a purchase panel from Purchase -> Configuration -> Purchase Panel
3. Select the panel from an agreement record.
4. Submit evaluation records for panel review/validation.

Screenshots are povided in the app description page.

## Versions

The app is built for Odoo versions `14.0` and `15.0` and has been tested on both community and enterprise versions. Branches are named after Odoo versions respectively.

## Roadmap

- Restrict bids until bid submission deadline.
- Score indvidual bids

## Issues and Suggestions

Please use the Issues tracker on this repo to report any issues or bugs. Please feel free to also use the issues tracker to suggest and make recommendations for more features or enhancements.

## Contribute

Contributions are most welcome - please feel free to fork the project, create a feature branch with the Odoo version mentioned, and open a pull request once changes are committed and pushed.

## License

App published under the LGPL v3 license - See <http://www.gnu.org/licenses/> for more details.
