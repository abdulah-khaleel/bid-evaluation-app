# Bid Evaluation App

Evaluate and Score Bids in Odoo

## Overview

This app extends the functionality of the 'Purchase Agreements' workflow within Odoo allowing you to evaluate individual bids recieved as part of a tender or a purchase agreement. It also provides the ability to create and use multiple evaluation templates, and setup each template with its own set of guidelines, checklists and evaluation/scoring criteria. An accompanying module enables the use of purchase panels for the evaluation process.

## Useage

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

Please refer to the app description page for screenshots.

## Versions

The app is tested on Odoo versions `14.0` and `15.0` for both community and enterprise versions. Branches are named after Odoo versions respectively.

## Roadmap

- Score indvidual bids
-

## Issues

Please use the Issues tracker on this repo to report any issues or bugs.

## Contribute

Contributions are most welcome - please feel free to fork the project, create a feature branch and open a pull request once changes are committed and pushed.

## License

App published under the LGPL v3 license - See <http://www.gnu.org/licenses/> for more details.
