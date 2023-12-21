# nium
NIUM Platform

- API version: 2023.12.5
- Package version: 1.0.0


## Requirements.

Python 3.7+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/nium-global/nium-python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/nium-global/nium-python.git`)

Then import the package:
```python
import nium
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import nium
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import time
import nium
from nium.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://gateway.nium.com
# See configuration.py for a list of all supported configuration parameters.
configuration = nium.Configuration(
    host = Environment.SANDBOX, 
    api_key = os.environ["API_KEY"]
)


# Enter a context with an instance of the API client
with nium.ApiClient(configuration) as nium_client:
    # Create an instance of the API class
    client_hash_id = 'client_hash_id_example' # str | Unique client identifier generated and shared before API handshake.
    customer_hash_id = 'customer_hash_id_example' # str | Unique customer identifier generated on customer creation.
    account_validation_request_dto = nium.AccountValidationRequestDTO() # AccountValidationRequestDTO | accountValidationRequestDTO
    x_request_id = '{{$guid}}' # str | Enter a unique UUID value. (optional)

    try:
        # Account verification (Confirmation of Payee)
        api_response = nium_client.beneficiary.account_verification(client_hash_id, customer_hash_id, account_validation_request_dto, x_request_id=x_request_id)
        print("The response of BeneficiaryApi->account_verification:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BeneficiaryApi->account_verification: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://gateway.nium.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*BeneficiaryApi* | [**account_verification**](docs/BeneficiaryApi.md#account_verification) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/accountVerification | Account verification (Confirmation of Payee)
*BeneficiaryApi* | [**add_beneficiary**](docs/BeneficiaryApi.md#add_beneficiary) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/beneficiaries | Add Beneficiary
*BeneficiaryApi* | [**add_beneficiary_v2**](docs/BeneficiaryApi.md#add_beneficiary_v2) | **POST** /api/v2/client/{clientHashId}/customer/{customerHashId}/beneficiaries | Add Beneficiary V2
*BeneficiaryApi* | [**beneficiary_details**](docs/BeneficiaryApi.md#beneficiary_details) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/beneficiaries/{beneficiaryHashId} | Beneficiary Details
*BeneficiaryApi* | [**beneficiary_details_v2**](docs/BeneficiaryApi.md#beneficiary_details_v2) | **GET** /api/v2/client/{clientHashId}/customer/{customerHashId}/beneficiaries/{beneficiaryHashId} | Beneficiary Details V2
*BeneficiaryApi* | [**beneficiary_list**](docs/BeneficiaryApi.md#beneficiary_list) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/beneficiaries | Beneficiary List
*BeneficiaryApi* | [**beneficiary_list_v2**](docs/BeneficiaryApi.md#beneficiary_list_v2) | **GET** /api/v2/client/{clientHashId}/customer/{customerHashId}/beneficiaries | Beneficiary List V2
*BeneficiaryApi* | [**beneficiary_validation_schema**](docs/BeneficiaryApi.md#beneficiary_validation_schema) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/currency/{currencyCode}/validationSchemas | Beneficiary Validation Schema
*BeneficiaryApi* | [**beneficiary_validation_schema_v2**](docs/BeneficiaryApi.md#beneficiary_validation_schema_v2) | **GET** /api/v2/client/{clientHashId}/customer/{customerHashId}/currency/{currencyCode}/validationSchemas | Beneficiary Validation Schema V2
*BeneficiaryApi* | [**confirmationof_payee**](docs/BeneficiaryApi.md#confirmationof_payee) | **POST** /api/v2/client/{clientHashId}/customer/{customerHashId}/beneficiaries/validate | Confirmation of Payee
*BeneficiaryApi* | [**delete_beneficiary**](docs/BeneficiaryApi.md#delete_beneficiary) | **DELETE** /api/v1/client/{clientHashId}/customer/{customerHashId}/beneficiaries/{beneficiaryHashId} | Delete Beneficiary
*BeneficiaryApi* | [**update_beneficiary**](docs/BeneficiaryApi.md#update_beneficiary) | **PUT** /api/v1/client/{clientHashId}/customer/{customerHashId}/beneficiaries/{beneficiaryHashId} | Update Beneficiary
*BeneficiaryApi* | [**update_beneficiary_v2**](docs/BeneficiaryApi.md#update_beneficiary_v2) | **PUT** /api/v2/client/{clientHashId}/customer/{customerHashId}/beneficiaries/{beneficiaryHashId} | Update Beneficiary V2
*CardsReferenceDataApi* | [**reference_exchange_rate**](docs/CardsReferenceDataApi.md#reference_exchange_rate) | **GET** /api/v1/client/{clientHashId}/referenceRate | Reference Exchange Rate
*ClientPrefundAccountApi* | [**client_prefund_balances**](docs/ClientPrefundAccountApi.md#client_prefund_balances) | **GET** /api/v1/client/{clientHashId}/balances | Client Prefund Balances
*ClientPrefundAccountApi* | [**client_prefund_request**](docs/ClientPrefundAccountApi.md#client_prefund_request) | **POST** /api/v1/client/{clientHashId}/prefund | Client Prefund Request
*ClientPrefundAccountApi* | [**fetch_client_prefund_request**](docs/ClientPrefundAccountApi.md#fetch_client_prefund_request) | **GET** /api/v1/client/{clientHashId}/prefundList | Fetch Client Prefund Request
*ClientSettingsApi* | [**client_details**](docs/ClientSettingsApi.md#client_details) | **GET** /api/v1/client/{clientHashId} | Client Details
*ClientSettingsApi* | [**fee_details**](docs/ClientSettingsApi.md#fee_details) | **GET** /api/v2/client/{clientHashId}/fees | Fee Details
*ClientTransactionsApi* | [**client_transactions**](docs/ClientTransactionsApi.md#client_transactions) | **GET** /api/v1/client/{clientHashId}/transactions | Client Transactions
*ControlsApi* | [**get_card_limits**](docs/ControlsApi.md#get_card_limits) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/limits | Fetch Card Limits
*ControlsApi* | [**get_channel_restriction**](docs/ControlsApi.md#get_channel_restriction) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/channels | Get Channel Restriction
*ControlsApi* | [**get_mcc_channel_restrictions**](docs/ControlsApi.md#get_mcc_channel_restrictions) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/channels/mcc | Get MCC Channel Restrictions
*ControlsApi* | [**limits_for_all_cards_for_a_customer**](docs/ControlsApi.md#limits_for_all_cards_for_a_customer) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/limits | Limits For All Cards For A Customer
*ControlsApi* | [**set_card_limits**](docs/ControlsApi.md#set_card_limits) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/limits | Card Limits
*ControlsApi* | [**update_channel_restriction**](docs/ControlsApi.md#update_channel_restriction) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/channels | Update Channel Restriction
*ControlsApi* | [**update_mcc_channel_restrictions**](docs/ControlsApi.md#update_mcc_channel_restrictions) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/channels/mcc | Update MCC Channel Restrictions
*ConversionsApi* | [**cancel_conversion**](docs/ConversionsApi.md#cancel_conversion) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/conversions/{conversionId}/cancel | Cancel Conversion
*ConversionsApi* | [**create_conversion**](docs/ConversionsApi.md#create_conversion) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/conversions | Create Conversion
*ConversionsApi* | [**fetch_conversion**](docs/ConversionsApi.md#fetch_conversion) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/conversions/{conversionId} | Fetch Conversion by id
*ConversionsPreviousVersionApi* | [**balance_transferwithin_wallet**](docs/ConversionsPreviousVersionApi.md#balance_transferwithin_wallet) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transfer | Balance Transfer within Wallet
*CustomerAccountCorporateApi* | [**exhaustive_corporate_details_using_business_id**](docs/CustomerAccountCorporateApi.md#exhaustive_corporate_details_using_business_id) | **GET** /api/v2/client/{clientHashId}/corporate/lookup | Exhaustive Corporate Details using Business ID
*CustomerAccountCorporateApi* | [**fetch_corporate_constants_using_get**](docs/CustomerAccountCorporateApi.md#fetch_corporate_constants_using_get) | **GET** /api/v2/client/{clientHashId}/onboarding/constants | Fetch corporate constants for category
*CustomerAccountCorporateApi* | [**fetch_corporate_customer_rfi_details**](docs/CustomerAccountCorporateApi.md#fetch_corporate_customer_rfi_details) | **GET** /api/v1/client/{clientHashId}/corporate/rfi | Fetch Corporate Customer RFI Details
*CustomerAccountCorporateApi* | [**onboard_corporate_customer**](docs/CustomerAccountCorporateApi.md#onboard_corporate_customer) | **POST** /api/v1/client/{clientHashId}/corporate | Onboard Corporate Customer
*CustomerAccountCorporateApi* | [**public_corporate_details_using_business_id**](docs/CustomerAccountCorporateApi.md#public_corporate_details_using_business_id) | **GET** /api/v1/client/{clientHashId}/corporate/lookup | Public Corporate Details using Business ID
*CustomerAccountCorporateApi* | [**regenerate_kycurl**](docs/CustomerAccountCorporateApi.md#regenerate_kycurl) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/regenerateKYCURL | Regenerate KYC URL
*CustomerAccountCorporateApi* | [**respondto_rf_ifor_corporate_customer**](docs/CustomerAccountCorporateApi.md#respondto_rf_ifor_corporate_customer) | **POST** /api/v1/client/{clientHashId}/corporate/rfi | Respond to RFI for Corporate Customer
*CustomerAccountCorporateApi* | [**update_corporate_customer_using_post**](docs/CustomerAccountCorporateApi.md#update_corporate_customer_using_post) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/corporate | Update Corporate KYB Flow
*CustomerAccountCorporateApi* | [**upload_documentfor_corporate_customer**](docs/CustomerAccountCorporateApi.md#upload_documentfor_corporate_customer) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/corporate/documents | Upload Document for Corporate Customer
*CustomerAccountIndividualApi* | [**add_customer**](docs/CustomerAccountIndividualApi.md#add_customer) | **POST** /api/v1/client/{clientHashId}/customer | Add Customer
*CustomerAccountIndividualApi* | [**add_customer_using_my_info_sg**](docs/CustomerAccountIndividualApi.md#add_customer_using_my_info_sg) | **POST** /api/v1/client/{clientHashId}/customer-min-data | Add Customer Using MyInfo [SG]
*CustomerAccountIndividualApi* | [**add_customer_usinge_document_verification**](docs/CustomerAccountIndividualApi.md#add_customer_usinge_document_verification) | **POST** /api/v3/client/{clientHashId}/customer | Add Customer Using e-Document Verification
*CustomerAccountIndividualApi* | [**customer_update**](docs/CustomerAccountIndividualApi.md#customer_update) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/updateCustomer | Customer Update
*CustomerAccountIndividualApi* | [**fetch_individual_customer_rfi_details**](docs/CustomerAccountIndividualApi.md#fetch_individual_customer_rfi_details) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/rfi | Fetch Individual Customer RFI Details
*CustomerAccountIndividualApi* | [**respondto_rfi**](docs/CustomerAccountIndividualApi.md#respondto_rfi) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/rfi | Respond to RFI
*CustomerAccountIndividualApi* | [**unified_add_customer**](docs/CustomerAccountIndividualApi.md#unified_add_customer) | **POST** /api/v4/client/{clientHashId}/customer | Unified Add Customer
*CustomerAccountIndividualApi* | [**upload_document**](docs/CustomerAccountIndividualApi.md#upload_document) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/uploadDocuments | Upload Document
*CustomerFeesApi* | [**charge_fee**](docs/CustomerFeesApi.md#charge_fee) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/fees | Charge Fee
*CustomerFundingApi* | [**add_funding_instrument**](docs/CustomerFundingApi.md#add_funding_instrument) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/fundingInstruments | Add funding instrument id
*CustomerFundingApi* | [**confirm_funding_instrument_id**](docs/CustomerFundingApi.md#confirm_funding_instrument_id) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/fundingInstruments/{fundingInstrumentId}/confirmFundingInstrument | Confirm funding instrument id
*CustomerFundingApi* | [**delete_fundinginstrument**](docs/CustomerFundingApi.md#delete_fundinginstrument) | **DELETE** /api/v1/client/{clientHashId}/customer/{customerHashId}/fundingInstruments/{fundingInstrumentId} | delete Funding instrument
*CustomerFundingApi* | [**fund_wallet**](docs/CustomerFundingApi.md#fund_wallet) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/fund | Fund Wallet
*CustomerFundingApi* | [**get_funding_instrument_details**](docs/CustomerFundingApi.md#get_funding_instrument_details) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/fundingInstruments/{fundingInstrumentId}/fundingInstrumentDetails | Get Funding instrument details
*CustomerFundingApi* | [**get_funding_instrument_list**](docs/CustomerFundingApi.md#get_funding_instrument_list) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/fundingInstruments | Get Funding Instrument List
*CustomerManagementApi* | [**account_statement**](docs/CustomerManagementApi.md#account_statement) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/accounts/statement | Account Statement
*CustomerManagementApi* | [**block_unblock_customer**](docs/CustomerManagementApi.md#block_unblock_customer) | **PUT** /api/v1/client/{clientHashId}/customer/{customerHashId}/block | Block/Unblock Customer
*CustomerManagementApi* | [**customer_details**](docs/CustomerManagementApi.md#customer_details) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId} | Customer Details
*CustomerManagementApi* | [**customer_details_v2**](docs/CustomerManagementApi.md#customer_details_v2) | **GET** /api/v2/client/{clientHashId}/customer/{customerHashId} | Customer Details V2
*CustomerManagementApi* | [**customer_list**](docs/CustomerManagementApi.md#customer_list) | **GET** /api/v1/client/{clientHashId}/customers | Customer List
*CustomerManagementApi* | [**customer_list_v2**](docs/CustomerManagementApi.md#customer_list_v2) | **GET** /api/v2/client/{clientHashId}/customers | Get Paginated Customer By Client And Optional Search Parameters.
*CustomerManagementApi* | [**customer_list_v3**](docs/CustomerManagementApi.md#customer_list_v3) | **GET** /api/v3/client/{clientHashId}/customers | Get Paginated Customer By Client And Optional Search Parameters.
*CustomerManagementApi* | [**manage_customer_tags**](docs/CustomerManagementApi.md#manage_customer_tags) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/tags | Manage Customer Tags
*CustomerTermsAndConditionsApi* | [**accept_termsand_conditions**](docs/CustomerTermsAndConditionsApi.md#accept_termsand_conditions) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/termsAndConditions | Accept Terms and Conditions
*CustomerTermsAndConditionsApi* | [**termsand_conditions**](docs/CustomerTermsAndConditionsApi.md#termsand_conditions) | **GET** /api/v1/client/{clientHashId}/termsAndConditions | Terms and Conditions
*CustomerVirtualAccountsApi* | [**account_ownership_certificate**](docs/CustomerVirtualAccountsApi.md#account_ownership_certificate) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/accountOwnershipCertificate | Account Ownership Certificate
*CustomerVirtualAccountsApi* | [**assign_payment_id**](docs/CustomerVirtualAccountsApi.md#assign_payment_id) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/paymentId | Assign Payment ID
*CustomerVirtualAccountsApi* | [**manage_virtual_account_tags**](docs/CustomerVirtualAccountsApi.md#manage_virtual_account_tags) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/paymentId/tags | Manage Virtual Account Tags
*CustomerVirtualAccountsApi* | [**virtual_account_details**](docs/CustomerVirtualAccountsApi.md#virtual_account_details) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/paymentIds | Virtual Account Details
*CustomerVirtualAccountsApi* | [**virtual_account_details_v2**](docs/CustomerVirtualAccountsApi.md#virtual_account_details_v2) | **GET** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/paymentIds | Virtual Account Details V2
*CustomerWalletBalanceApi* | [**wallet_balance**](docs/CustomerWalletBalanceApi.md#wallet_balance) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId} | Wallet Balance
*CustomerWalletTransactionsApi* | [**download_transaction_receipt**](docs/CustomerWalletTransactionsApi.md#download_transaction_receipt) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transactions/{transactionId}/receipt | Download Transaction Receipt
*CustomerWalletTransactionsApi* | [**manage_transaction_tags**](docs/CustomerWalletTransactionsApi.md#manage_transaction_tags) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transactions/{transactionId}/tags | Manage Transaction Tags
*CustomerWalletTransactionsApi* | [**transaction_geo_tagging**](docs/CustomerWalletTransactionsApi.md#transaction_geo_tagging) | **PUT** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transactions/{transactionId}/location | Transaction Geo-Tagging
*CustomerWalletTransactionsApi* | [**transactions**](docs/CustomerWalletTransactionsApi.md#transactions) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transactions | Transactions
*CustomerWalletTransactionsApi* | [**update_business_transaction_flag**](docs/CustomerWalletTransactionsApi.md#update_business_transaction_flag) | **PUT** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transactions/{transactionId}/business | Update Business Transaction Flag
*CustomerWalletTransactionsApi* | [**upload_transaction_receipt**](docs/CustomerWalletTransactionsApi.md#upload_transaction_receipt) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transactions/{transactionId}/receipt | Upload Transaction Receipt
*LifecycleApi* | [**activate_card**](docs/LifecycleApi.md#activate_card) | **POST** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/activate | Activate Card
*LifecycleApi* | [**activate_card1**](docs/LifecycleApi.md#activate_card1) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/activate | Activate Card
*LifecycleApi* | [**add_card**](docs/LifecycleApi.md#add_card) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card | Add Card
*LifecycleApi* | [**add_card_v2**](docs/LifecycleApi.md#add_card_v2) | **POST** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card | Add Card V2
*LifecycleApi* | [**assign_card**](docs/LifecycleApi.md#assign_card) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/assignCard | Assign Card
*LifecycleApi* | [**block_and_replace_card_v2**](docs/LifecycleApi.md#block_and_replace_card_v2) | **POST** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/blockAndReplace | Block and Replace Card V2
*LifecycleApi* | [**block_unblock_cards**](docs/LifecycleApi.md#block_unblock_cards) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/cardAction | Block/Unblock Cards
*LifecycleApi* | [**card_details**](docs/LifecycleApi.md#card_details) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId} | Card Details
*LifecycleApi* | [**card_details_v2**](docs/LifecycleApi.md#card_details_v2) | **GET** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId} | Card Details V2
*LifecycleApi* | [**card_list**](docs/LifecycleApi.md#card_list) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/cards | Card List
*LifecycleApi* | [**card_list_v2**](docs/LifecycleApi.md#card_list_v2) | **GET** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/cards | Card List V2
*LifecycleApi* | [**get_card_widget**](docs/LifecycleApi.md#get_card_widget) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/widget/showCardDetails | Get Card Details Widget
*LifecycleApi* | [**issue_replacement_card**](docs/LifecycleApi.md#issue_replacement_card) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/replaceCard | Issue Replacement Card
*LifecycleApi* | [**lock_unlock_card_v2**](docs/LifecycleApi.md#lock_unlock_card_v2) | **PUT** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/lockAction | Lock/Unlock Card V2
*LifecycleApi* | [**renew_card**](docs/LifecycleApi.md#renew_card) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/renewCard | Renew Card
*LifecycleApi* | [**update_card_details_v2**](docs/LifecycleApi.md#update_card_details_v2) | **POST** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId} | Update Card Details V2
*NewCorporateAPIsApi* | [**regenerate_kycurl1**](docs/NewCorporateAPIsApi.md#regenerate_kycurl1) | **POST** /api/v1/client/{clientHashId}/customer/corporate/application/{applicationId}/regenerateKYCURL | Regenerate KYC URL
*OpenBankingOnboardingApi* | [**account_details_by_customer_consent_id**](docs/OpenBankingOnboardingApi.md#account_details_by_customer_consent_id) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/consent/account | Account Details By Customer Consent ID.
*OpenBankingOnboardingApi* | [**payment_detailsby_system_reference_number**](docs/OpenBankingOnboardingApi.md#payment_detailsby_system_reference_number) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/consent/payment | Payment Details by System Reference Number
*PayinApi* | [**simulate_funding_instrument_status_update**](docs/PayinApi.md#simulate_funding_instrument_status_update) | **POST** /api/v1/simulations/client/{clientHashId}/customer/{customerHashId}/fundingInstruments/{fundingInstrumentId}/updateStatus | Simulate Funding Instrument Status Update (Sandbox Testing)
*PayinApi* | [**simulatereceivepayment**](docs/PayinApi.md#simulatereceivepayment) | **POST** /api/v1/inward/payment/manual | Manual ICC process
*PayoutApi* | [**customer_get_card_widget**](docs/PayoutApi.md#customer_get_card_widget) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/widget/token | Get Card Widget
*PayoutApi* | [**fetch_remittance_life_cycle_status**](docs/PayoutApi.md#fetch_remittance_life_cycle_status) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/remittance/{systemReferenceNumber}/audit | Fetch Remittance Life Cycle Status
*PayoutApi* | [**po_p**](docs/PayoutApi.md#po_p) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/remittance/{systemReferenceNumber}/receipt | Get Proof Of Payment
*PayoutApi* | [**purposeof_transfer**](docs/PayoutApi.md#purposeof_transfer) | **GET** /api/v1/remittance/purposeCodes | Purpose of Transfer
*PayoutApi* | [**respondto_transaction_rfi**](docs/PayoutApi.md#respondto_transaction_rfi) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transactions/{authCode}/rfi/upload | Respond to Transaction RFI
*PayoutApi* | [**transfer_money**](docs/PayoutApi.md#transfer_money) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/remittance | Transfer Money
*PayoutApi* | [**withdraw_funds_from_wallet**](docs/PayoutApi.md#withdraw_funds_from_wallet) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/refund | Withdraw Funds from Wallet
*QuotesApi* | [**create_quote**](docs/QuotesApi.md#create_quote) | **POST** /api/v1/client/{clientHashId}/quotes | Create Quote
*QuotesApi* | [**fetch_quote**](docs/QuotesApi.md#fetch_quote) | **GET** /api/v1/client/{clientHashId}/quotes/{quoteId} | Fetch Quote by ID
*QuotesPreviousVersionApi* | [**exchange_rate_lockand_hold**](docs/QuotesPreviousVersionApi.md#exchange_rate_lockand_hold) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/lockExchangeRate | Exchange Rate Lock and Hold
*QuotesPreviousVersionApi* | [**exchange_rate_with_markup**](docs/QuotesPreviousVersionApi.md#exchange_rate_with_markup) | **GET** /api/v1/client/{clientHashId}/exchangeRate | Exchange Rate With Markup
*RatesApi* | [**aggregated_exchange_rates**](docs/RatesApi.md#aggregated_exchange_rates) | **GET** /api/v1/exchangeRates/aggregate | Fetch historic aggregate exchange rates
*RatesApi* | [**exchange_rate_v2**](docs/RatesApi.md#exchange_rate_v2) | **GET** /api/v2/exchangeRate | Exchange Rate V2
*ReferenceDataApi* | [**fetch_bank_detailsusing_routing_code**](docs/ReferenceDataApi.md#fetch_bank_detailsusing_routing_code) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/country/{countryCode}/routingCodeType/{routingCodeType}/routingCodeValue/{routingCodeValue}/routingCode | Fetch Bank Details using Routing Code
*ReferenceDataApi* | [**fetch_supported_corridors**](docs/ReferenceDataApi.md#fetch_supported_corridors) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/supportedCorridors | Fetch Supported Corridors
*ReferenceDataApi* | [**fetch_supported_corridors_v2**](docs/ReferenceDataApi.md#fetch_supported_corridors_v2) | **GET** /api/v2/client/{clientHashId}/supportedCorridors | Fetch Supported Corridors V2
*ReferenceDataApi* | [**search_routing_code_using_bank_name**](docs/ReferenceDataApi.md#search_routing_code_using_bank_name) | **GET** /api/v2/client/{clientHashId}/payout/banks | Search Routing Code Using Bank Name
*ReferenceDataApi* | [**search_routing_code_using_branch_name**](docs/ReferenceDataApi.md#search_routing_code_using_branch_name) | **GET** /api/v2/client/{clientHashId}/payout/branches | Search Routing Code Using Branch Name
*ReferenceDataApi* | [**search_routing_codeusingbanknamebranchname**](docs/ReferenceDataApi.md#search_routing_codeusingbanknamebranchname) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/partialSearch | Search Routing Code (using bank name/branch name)
*SecurityApi* | [**fetch_atm_pin**](docs/SecurityApi.md#fetch_atm_pin) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/pin | Fetch ATM Pin
*SecurityApi* | [**fetch_card_data_encrypted_v2**](docs/SecurityApi.md#fetch_card_data_encrypted_v2) | **GET** /api/v2/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/retrieve | Fetch Card Data Encrypted V2
*SecurityApi* | [**fetch_cvv2**](docs/SecurityApi.md#fetch_cvv2) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/cvv | Fetch CVV2
*SecurityApi* | [**fetch_pin_status**](docs/SecurityApi.md#fetch_pin_status) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/pin/status | Fetch Pin Status
*SecurityApi* | [**set_reset_pin**](docs/SecurityApi.md#set_reset_pin) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/pin | Set/Reset PIN
*SecurityApi* | [**unblock_card_pin**](docs/SecurityApi.md#unblock_card_pin) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/pin/unblock | Unblock PIN
*SecurityApi* | [**unmask_card**](docs/SecurityApi.md#unmask_card) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/unmask | Unmask Card
*SimulatorsApi* | [**simulate_authorization**](docs/SimulatorsApi.md#simulate_authorization) | **POST** /api/v1/txn | This API will be used to Authorize a transaction
*SimulatorsApi* | [**simulate_clearing**](docs/SimulatorsApi.md#simulate_clearing) | **POST** /api/v1/settlement/run | This API will be used to run a given settlement
*ThreeDSApi* | [**passcode_enrollment_status**](docs/ThreeDSApi.md#passcode_enrollment_status) | **GET** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/3ds/passcode/status | 3DS Client passcode enrollment status
*ThreeDSApi* | [**process_oo_bcallback**](docs/ThreeDSApi.md#process_oo_bcallback) | **POST** /api/v1/client/{clientHashId}/notifications/3ds/oob/callback | Process OOB callback
*ThreeDSApi* | [**process_oob_callback_v2**](docs/ThreeDSApi.md#process_oob_callback_v2) | **POST** /api/v2/client/{clientHashId}/3ds/oob/callback | 3DS OOB Callback V2
*ThreeDSApi* | [**set_passcode**](docs/ThreeDSApi.md#set_passcode) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/card/{cardHashId}/3ds/passcode | Add or Update passcode
*WalletToWalletTransfersApi* | [**p2_p_transfer**](docs/WalletToWalletTransfersApi.md#p2_p_transfer) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/p2pTransfer | P2P Transfer
*WalletToWalletTransfersApi* | [**wallet_transfer**](docs/WalletToWalletTransfersApi.md#wallet_transfer) | **POST** /api/v1/client/{clientHashId}/customer/{customerHashId}/wallet/{walletHashId}/transfers | InterClient Wallet Transfer
*PayoutControllerApi* | [**fetch_supported_corridors_v3**](docs/PayoutControllerApi.md#fetch_supported_corridors_v3) | **GET** /api/v3/client/{clientHashId}/supportedCorridors | Fetch Supported Corridors V3


## Documentation For Models

 - [Access](docs/Access.md)
 - [Account](docs/Account.md)
 - [AccountReference](docs/AccountReference.md)
 - [AccountResponseDTO](docs/AccountResponseDTO.md)
 - [AccountStatusResponse](docs/AccountStatusResponse.md)
 - [AccountValidationRequestDTO](docs/AccountValidationRequestDTO.md)
 - [AccountValidationResponseDTO](docs/AccountValidationResponseDTO.md)
 - [ActivateCardRequestV2DTO](docs/ActivateCardRequestV2DTO.md)
 - [ActivateCardResponseDTO](docs/ActivateCardResponseDTO.md)
 - [ActivateCardResponseV2DTO](docs/ActivateCardResponseV2DTO.md)
 - [AddBeneficiaryRequest](docs/AddBeneficiaryRequest.md)
 - [AddBeneficiaryRequestDTO](docs/AddBeneficiaryRequestDTO.md)
 - [AddCardRequest](docs/AddCardRequest.md)
 - [AddCardRequestV2](docs/AddCardRequestV2.md)
 - [AddCardResponseDTO](docs/AddCardResponseDTO.md)
 - [AddCardV2ResponseDTO](docs/AddCardV2ResponseDTO.md)
 - [AddCategoryResponseDTO](docs/AddCategoryResponseDTO.md)
 - [AddCustomerRequestDTO](docs/AddCustomerRequestDTO.md)
 - [AddCustomerResponseDTO](docs/AddCustomerResponseDTO.md)
 - [AdditionalFeesDTO](docs/AdditionalFeesDTO.md)
 - [Address](docs/Address.md)
 - [AddressDTO](docs/AddressDTO.md)
 - [AddressV2](docs/AddressV2.md)
 - [Addresses](docs/Addresses.md)
 - [Amount](docs/Amount.md)
 - [ApiError](docs/ApiError.md)
 - [ApiError2](docs/ApiError2.md)
 - [ApiResponse2](docs/ApiResponse2.md)
 - [ApiResponseOfTransactionChannelsResponseDTO](docs/ApiResponseOfTransactionChannelsResponseDTO.md)
 - [ApiResponseOfWalletRefundResponseDTO](docs/ApiResponseOfWalletRefundResponseDTO.md)
 - [ApiResponseOfstring](docs/ApiResponseOfstring.md)
 - [ApplicantDetails](docs/ApplicantDetails.md)
 - [ApplicantDetails2](docs/ApplicantDetails2.md)
 - [ApplicantDetailsV2](docs/ApplicantDetailsV2.md)
 - [ApplicationCommonResponse](docs/ApplicationCommonResponse.md)
 - [AssignCardDTO](docs/AssignCardDTO.md)
 - [AssociationDetails](docs/AssociationDetails.md)
 - [AutoSweepBankDetails](docs/AutoSweepBankDetails.md)
 - [Balance](docs/Balance.md)
 - [BalanceAmount](docs/BalanceAmount.md)
 - [BankAccountDetails](docs/BankAccountDetails.md)
 - [BankRoutingInfo](docs/BankRoutingInfo.md)
 - [Beneficiary](docs/Beneficiary.md)
 - [BeneficiaryAccountDetailsDTO](docs/BeneficiaryAccountDetailsDTO.md)
 - [BeneficiaryDetailRequest](docs/BeneficiaryDetailRequest.md)
 - [BeneficiaryDetailsDTO](docs/BeneficiaryDetailsDTO.md)
 - [BeneficiaryResponseDTO](docs/BeneficiaryResponseDTO.md)
 - [BeneficiaryValidationRequestDTO](docs/BeneficiaryValidationRequestDTO.md)
 - [BeneficiaryValidationResponseDTO](docs/BeneficiaryValidationResponseDTO.md)
 - [BlockAndReplaceCardRequestDTO](docs/BlockAndReplaceCardRequestDTO.md)
 - [BlockAndReplaceCardResponseDTO](docs/BlockAndReplaceCardResponseDTO.md)
 - [BlockAndReplaceStatus](docs/BlockAndReplaceStatus.md)
 - [BlockCodeCardResponseDTO](docs/BlockCodeCardResponseDTO.md)
 - [BlockCodeDTO](docs/BlockCodeDTO.md)
 - [BlockCustomerRequestDTO](docs/BlockCustomerRequestDTO.md)
 - [BranchNameResponseDTO](docs/BranchNameResponseDTO.md)
 - [BusinessAddress](docs/BusinessAddress.md)
 - [BusinessDetails](docs/BusinessDetails.md)
 - [BusinessDetails2](docs/BusinessDetails2.md)
 - [BusinessDetailsResponseDTO](docs/BusinessDetailsResponseDTO.md)
 - [BusinessDetailsResponseV2DTO](docs/BusinessDetailsResponseV2DTO.md)
 - [BusinessPartner](docs/BusinessPartner.md)
 - [BusinessPartner2](docs/BusinessPartner2.md)
 - [BusinessPartnerAddresses](docs/BusinessPartnerAddresses.md)
 - [BusinessPartnerDetailsResponseDTO](docs/BusinessPartnerDetailsResponseDTO.md)
 - [BusinessPartnerLegalDetails](docs/BusinessPartnerLegalDetails.md)
 - [BusinessPartnerV2](docs/BusinessPartnerV2.md)
 - [ButtonDTO](docs/ButtonDTO.md)
 - [CSSAttributeDTO](docs/CSSAttributeDTO.md)
 - [CancelConversionError](docs/CancelConversionError.md)
 - [CancelConversionErrorResponse](docs/CancelConversionErrorResponse.md)
 - [CancellationReason](docs/CancellationReason.md)
 - [CardAcceptorAddress](docs/CardAcceptorAddress.md)
 - [CardAssignResponseDTO](docs/CardAssignResponseDTO.md)
 - [CardDetails](docs/CardDetails.md)
 - [CardInfo](docs/CardInfo.md)
 - [CardMetaDataResponseDTO](docs/CardMetaDataResponseDTO.md)
 - [CardResponseDTO](docs/CardResponseDTO.md)
 - [CardTokensDTO](docs/CardTokensDTO.md)
 - [CardWidgetTokenRequestDTO](docs/CardWidgetTokenRequestDTO.md)
 - [CardWidgetTokenResponse](docs/CardWidgetTokenResponse.md)
 - [CategoryData](docs/CategoryData.md)
 - [ChannelActionRequestDTO](docs/ChannelActionRequestDTO.md)
 - [ClientCurrencyResponseDTO](docs/ClientCurrencyResponseDTO.md)
 - [ClientCustomTagDTO](docs/ClientCustomTagDTO.md)
 - [ClientDetailResponseDTO2](docs/ClientDetailResponseDTO2.md)
 - [ClientFeeDetailsResponseDTO](docs/ClientFeeDetailsResponseDTO.md)
 - [ClientPrefundResponseDTO](docs/ClientPrefundResponseDTO.md)
 - [ClientTransactionsResponseDTO](docs/ClientTransactionsResponseDTO.md)
 - [CommonResponse](docs/CommonResponse.md)
 - [ComplianceDocumentDTO](docs/ComplianceDocumentDTO.md)
 - [ComplianceDocumentResponseDTO](docs/ComplianceDocumentResponseDTO.md)
 - [ComplianceIdentificationDocDTO](docs/ComplianceIdentificationDocDTO.md)
 - [ComplianceRFITemplateMetadataResponseDTO](docs/ComplianceRFITemplateMetadataResponseDTO.md)
 - [ConfirmFundingInstrumentRequestDTO](docs/ConfirmFundingInstrumentRequestDTO.md)
 - [Consent](docs/Consent.md)
 - [ConsentDetailsResponse](docs/ConsentDetailsResponse.md)
 - [ContactDetails](docs/ContactDetails.md)
 - [ContactDetailsResponseDTO](docs/ContactDetailsResponseDTO.md)
 - [ContainerDTO](docs/ContainerDTO.md)
 - [ConversionCancelRequest](docs/ConversionCancelRequest.md)
 - [ConversionCancelResponse](docs/ConversionCancelResponse.md)
 - [ConversionCreationRequest](docs/ConversionCreationRequest.md)
 - [ConversionCreationResponse](docs/ConversionCreationResponse.md)
 - [ConversionSchedule](docs/ConversionSchedule.md)
 - [ConversionStatus](docs/ConversionStatus.md)
 - [CorporateAddress](docs/CorporateAddress.md)
 - [CorporateAddressDTO](docs/CorporateAddressDTO.md)
 - [CorporateAddresses](docs/CorporateAddresses.md)
 - [CorporateBusinessDetails](docs/CorporateBusinessDetails.md)
 - [CorporateBusinessDetailsDocumentDetailDTO](docs/CorporateBusinessDetailsDocumentDetailDTO.md)
 - [CorporateBusinessPartner](docs/CorporateBusinessPartner.md)
 - [CorporateBusinessPartnerLegalDetails](docs/CorporateBusinessPartnerLegalDetails.md)
 - [CorporateComplianceDocumentRequestDTO](docs/CorporateComplianceDocumentRequestDTO.md)
 - [CorporateComplianceDocumentResponseDTO](docs/CorporateComplianceDocumentResponseDTO.md)
 - [CorporateContactDetails](docs/CorporateContactDetails.md)
 - [CorporateCustomerRequestsDTO](docs/CorporateCustomerRequestsDTO.md)
 - [CorporateCustomerResponseDTO](docs/CorporateCustomerResponseDTO.md)
 - [CorporateDetailResponseDTO](docs/CorporateDetailResponseDTO.md)
 - [CorporateDocumentDetail](docs/CorporateDocumentDetail.md)
 - [CorporateDocumentDetails2DTO](docs/CorporateDocumentDetails2DTO.md)
 - [CorporateDocumentDetailsDTO](docs/CorporateDocumentDetailsDTO.md)
 - [CorporateDocumentUploadApplicantDetailsDTO](docs/CorporateDocumentUploadApplicantDetailsDTO.md)
 - [CorporateDocumentUploadBusinessDetailsDTO](docs/CorporateDocumentUploadBusinessDetailsDTO.md)
 - [CorporateDocumentUploadStakeholderDetailsDTO](docs/CorporateDocumentUploadStakeholderDetailsDTO.md)
 - [CorporateDocumentUploadStakeholdersDTO](docs/CorporateDocumentUploadStakeholdersDTO.md)
 - [CorporateEnrichedDetailResponseDTO](docs/CorporateEnrichedDetailResponseDTO.md)
 - [CorporateLegalDetails](docs/CorporateLegalDetails.md)
 - [CorporateProfessionalDetails](docs/CorporateProfessionalDetails.md)
 - [CorporateRegisteredAddress](docs/CorporateRegisteredAddress.md)
 - [CorporateRiskAssessmentInfo](docs/CorporateRiskAssessmentInfo.md)
 - [CorporateStakeholderDetails](docs/CorporateStakeholderDetails.md)
 - [CorporateStakeholders](docs/CorporateStakeholders.md)
 - [CreateConversionError](docs/CreateConversionError.md)
 - [CreateConversionErrorResponse](docs/CreateConversionErrorResponse.md)
 - [CreateQuoteError](docs/CreateQuoteError.md)
 - [CreateQuoteErrorResponse](docs/CreateQuoteErrorResponse.md)
 - [CustomFeeRequestDTO](docs/CustomFeeRequestDTO.md)
 - [CustomFeeResponseDTO](docs/CustomFeeResponseDTO.md)
 - [CustomerAccountDetail](docs/CustomerAccountDetail.md)
 - [CustomerApiError](docs/CustomerApiError.md)
 - [CustomerCardWidgetTokenRequestDTO](docs/CustomerCardWidgetTokenRequestDTO.md)
 - [CustomerCardWidgetTokenResponse](docs/CustomerCardWidgetTokenResponse.md)
 - [CustomerClientTagRequestDTO](docs/CustomerClientTagRequestDTO.md)
 - [CustomerClientTagResponseDTO](docs/CustomerClientTagResponseDTO.md)
 - [CustomerClientTagsRequestDTO](docs/CustomerClientTagsRequestDTO.md)
 - [CustomerClientTagsResponseDTO](docs/CustomerClientTagsResponseDTO.md)
 - [CustomerDataExternalRequestDTO](docs/CustomerDataExternalRequestDTO.md)
 - [CustomerDataExternalResponseDTO](docs/CustomerDataExternalResponseDTO.md)
 - [CustomerDataRequestDTO](docs/CustomerDataRequestDTO.md)
 - [CustomerDetailResponse](docs/CustomerDetailResponse.md)
 - [CustomerDetailResponseDTO](docs/CustomerDetailResponseDTO.md)
 - [CustomerDetailsResponseV2DTO](docs/CustomerDetailsResponseV2DTO.md)
 - [CustomerLinkAccountRequest](docs/CustomerLinkAccountRequest.md)
 - [CustomerRfiDetailsResponse](docs/CustomerRfiDetailsResponse.md)
 - [CustomerTagDTO](docs/CustomerTagDTO.md)
 - [CustomerTaxDetailDTO](docs/CustomerTaxDetailDTO.md)
 - [CvvResponseDTO](docs/CvvResponseDTO.md)
 - [Demographics](docs/Demographics.md)
 - [DeviceDetailsDTO](docs/DeviceDetailsDTO.md)
 - [Document](docs/Document.md)
 - [DocumentDetail](docs/DocumentDetail.md)
 - [EVerifyCustomerRegistrationRequestDTO](docs/EVerifyCustomerRegistrationRequestDTO.md)
 - [EitherSourceOrDestinationAmount](docs/EitherSourceOrDestinationAmount.md)
 - [EitherSourceOrDestinationAmountOrNoAmount](docs/EitherSourceOrDestinationAmountOrNoAmount.md)
 - [EmbossingDetails](docs/EmbossingDetails.md)
 - [Error](docs/Error.md)
 - [ErrorCodeMapping](docs/ErrorCodeMapping.md)
 - [ErrorCodes400](docs/ErrorCodes400.md)
 - [ErrorCodes401](docs/ErrorCodes401.md)
 - [ErrorCodes403](docs/ErrorCodes403.md)
 - [ErrorCodes500](docs/ErrorCodes500.md)
 - [ErrorDetail400](docs/ErrorDetail400.md)
 - [ErrorDetail401](docs/ErrorDetail401.md)
 - [ErrorDetail403](docs/ErrorDetail403.md)
 - [ErrorDetail500](docs/ErrorDetail500.md)
 - [ErrorResponse400](docs/ErrorResponse400.md)
 - [ErrorResponse401](docs/ErrorResponse401.md)
 - [ErrorResponse403](docs/ErrorResponse403.md)
 - [ErrorResponse500](docs/ErrorResponse500.md)
 - [ExchangeRateGetResponse](docs/ExchangeRateGetResponse.md)
 - [ExchangeRateV2ResponseDto](docs/ExchangeRateV2ResponseDto.md)
 - [ExchangeRatesGetResponse](docs/ExchangeRatesGetResponse.md)
 - [FXStandard401Error](docs/FXStandard401Error.md)
 - [FXStandard403Error](docs/FXStandard403Error.md)
 - [FXStandard500Error](docs/FXStandard500Error.md)
 - [FeeResponseDTO](docs/FeeResponseDTO.md)
 - [FetchConversionError](docs/FetchConversionError.md)
 - [FetchConversionErrorResponse](docs/FetchConversionErrorResponse.md)
 - [FetchPinResponseDTO](docs/FetchPinResponseDTO.md)
 - [FetchPinStatusResponseDTO](docs/FetchPinStatusResponseDTO.md)
 - [FetchQuoteError](docs/FetchQuoteError.md)
 - [FetchQuoteErrorResponse](docs/FetchQuoteErrorResponse.md)
 - [File](docs/File.md)
 - [FundTransferRequestDTO](docs/FundTransferRequestDTO.md)
 - [FundTransferResponse](docs/FundTransferResponse.md)
 - [FundingInstrumentStatusUpdateRequestDTO](docs/FundingInstrumentStatusUpdateRequestDTO.md)
 - [FxHoldLockResponseContent](docs/FxHoldLockResponseContent.md)
 - [GPIResponseDTO](docs/GPIResponseDTO.md)
 - [IdentificationDocDTO](docs/IdentificationDocDTO.md)
 - [IdentificationDocumentDTO](docs/IdentificationDocumentDTO.md)
 - [IndividualCustomerResponseDTO](docs/IndividualCustomerResponseDTO.md)
 - [InputFieldDTO](docs/InputFieldDTO.md)
 - [InvoiceDetails](docs/InvoiceDetails.md)
 - [InwardPaymentManualRequestDTO](docs/InwardPaymentManualRequestDTO.md)
 - [ItemDetails](docs/ItemDetails.md)
 - [Labels](docs/Labels.md)
 - [LegalDetails](docs/LegalDetails.md)
 - [LegalDetailsV2](docs/LegalDetailsV2.md)
 - [LinkAccountResponse](docs/LinkAccountResponse.md)
 - [LocalIsoRequest](docs/LocalIsoRequest.md)
 - [LocalIsoResponse](docs/LocalIsoResponse.md)
 - [LockPeriod](docs/LockPeriod.md)
 - [LockStatusUpdateRequestDTO](docs/LockStatusUpdateRequestDTO.md)
 - [LockStatusUpdateResponseDTO](docs/LockStatusUpdateResponseDTO.md)
 - [MCCRestrictionDTO](docs/MCCRestrictionDTO.md)
 - [MerchantCategoryResponseDTO2](docs/MerchantCategoryResponseDTO2.md)
 - [NewErrorResponse](docs/NewErrorResponse.md)
 - [OOBCallbackResponseDTO](docs/OOBCallbackResponseDTO.md)
 - [OnboardingDetails](docs/OnboardingDetails.md)
 - [OobCallbackRequestDTO](docs/OobCallbackRequestDTO.md)
 - [OpenBankingPaymentResponseDTO](docs/OpenBankingPaymentResponseDTO.md)
 - [P2PTransferDTO](docs/P2PTransferDTO.md)
 - [P2PTransferResponse](docs/P2PTransferResponse.md)
 - [PageResponseCardDetails](docs/PageResponseCardDetails.md)
 - [PaginatedCustomerDetailsResponseV2DTO](docs/PaginatedCustomerDetailsResponseV2DTO.md)
 - [PaginatedResponseDTOCustomerDetailsResponseV2DTO](docs/PaginatedResponseDTOCustomerDetailsResponseV2DTO.md)
 - [Pagination](docs/Pagination.md)
 - [PartialSearchBankNameResponseDTO](docs/PartialSearchBankNameResponseDTO.md)
 - [PartialSearchBranchNameResponseDTO](docs/PartialSearchBranchNameResponseDTO.md)
 - [PartialSearchDTO](docs/PartialSearchDTO.md)
 - [PartnershipDetails](docs/PartnershipDetails.md)
 - [PasscodeRequestDTO](docs/PasscodeRequestDTO.md)
 - [PasscodeResponseDTO](docs/PasscodeResponseDTO.md)
 - [PasscodeStatusDTO](docs/PasscodeStatusDTO.md)
 - [PayinApiError](docs/PayinApiError.md)
 - [PayinApiResponse2](docs/PayinApiResponse2.md)
 - [Payment](docs/Payment.md)
 - [PaymentIdCientTagsResponseDTO](docs/PaymentIdCientTagsResponseDTO.md)
 - [PaymentIdClientTagResponseDTO](docs/PaymentIdClientTagResponseDTO.md)
 - [PaymentIdDTO](docs/PaymentIdDTO.md)
 - [PaymentIdRequestDTO2](docs/PaymentIdRequestDTO2.md)
 - [PaymentIdResponseDTO2](docs/PaymentIdResponseDTO2.md)
 - [PaymentIdTagRequestDTO](docs/PaymentIdTagRequestDTO.md)
 - [PaymentIdsDTO](docs/PaymentIdsDTO.md)
 - [Payout](docs/Payout.md)
 - [PayoutRequest](docs/PayoutRequest.md)
 - [PayoutUploadRfiDetailsResponseDTO](docs/PayoutUploadRfiDetailsResponseDTO.md)
 - [PayoutUploadRfiDocumentRequestDTO](docs/PayoutUploadRfiDocumentRequestDTO.md)
 - [PinUpdateRequestDTO](docs/PinUpdateRequestDTO.md)
 - [PinUpdateResponseDTO](docs/PinUpdateResponseDTO.md)
 - [PrefundRequestDTO](docs/PrefundRequestDTO.md)
 - [ProductAddress](docs/ProductAddress.md)
 - [ProductApiError](docs/ProductApiError.md)
 - [ProductAssociationDetails](docs/ProductAssociationDetails.md)
 - [ProductCorporateCustomerResponseDTO](docs/ProductCorporateCustomerResponseDTO.md)
 - [ProductCustomerTagDTO](docs/ProductCustomerTagDTO.md)
 - [ProductDocument](docs/ProductDocument.md)
 - [ProductDocumentDetail](docs/ProductDocumentDetail.md)
 - [ProductPartnershipDetails](docs/ProductPartnershipDetails.md)
 - [ProductProfessionalDetails](docs/ProductProfessionalDetails.md)
 - [ProductRegulatoryDetails](docs/ProductRegulatoryDetails.md)
 - [ProductRfiResponseRequest](docs/ProductRfiResponseRequest.md)
 - [ProductTaxDetails](docs/ProductTaxDetails.md)
 - [ProfessionalDetails](docs/ProfessionalDetails.md)
 - [ProfessionalDetailsResponseDTO](docs/ProfessionalDetailsResponseDTO.md)
 - [PublicCorporateBusinessDetails](docs/PublicCorporateBusinessDetails.md)
 - [PurposeCodeResponseDTO](docs/PurposeCodeResponseDTO.md)
 - [QuoteCreationRequest](docs/QuoteCreationRequest.md)
 - [QuoteCreationResponse](docs/QuoteCreationResponse.md)
 - [QuoteType](docs/QuoteType.md)
 - [ReferenceRateResponseDto](docs/ReferenceRateResponseDto.md)
 - [RegenerateKYCURL400Response](docs/RegenerateKYCURL400Response.md)
 - [RegenerateUrlResponse](docs/RegenerateUrlResponse.md)
 - [RegisteredAddress](docs/RegisteredAddress.md)
 - [RegulatoryDetails](docs/RegulatoryDetails.md)
 - [RemittanceEventsResponseDTO2](docs/RemittanceEventsResponseDTO2.md)
 - [RemittanceResponseDTO](docs/RemittanceResponseDTO.md)
 - [RemittanceTransactionsRequestDTO](docs/RemittanceTransactionsRequestDTO.md)
 - [RemitterAccountWhiteList](docs/RemitterAccountWhiteList.md)
 - [RemitterRequestDTO](docs/RemitterRequestDTO.md)
 - [RenewCardRequest](docs/RenewCardRequest.md)
 - [ReplaceCardRequest](docs/ReplaceCardRequest.md)
 - [RequiredFields](docs/RequiredFields.md)
 - [Resource](docs/Resource.md)
 - [RespondRfiRequestDTO](docs/RespondRfiRequestDTO.md)
 - [RespondRfiResponseDTO](docs/RespondRfiResponseDTO.md)
 - [Result](docs/Result.md)
 - [RetrieveCardDetailsResponseDTO](docs/RetrieveCardDetailsResponseDTO.md)
 - [RevenueInfo](docs/RevenueInfo.md)
 - [RfiAttributeResponse](docs/RfiAttributeResponse.md)
 - [RfiIdentificationDoc](docs/RfiIdentificationDoc.md)
 - [RfiResponseInfo](docs/RfiResponseInfo.md)
 - [RfiResponseRequest](docs/RfiResponseRequest.md)
 - [RfiTemplate](docs/RfiTemplate.md)
 - [RiskAssessmentInfo](docs/RiskAssessmentInfo.md)
 - [RiskAssessmentInfoResponseDTO](docs/RiskAssessmentInfoResponseDTO.md)
 - [RiskAssessmentInfoV2](docs/RiskAssessmentInfoV2.md)
 - [RoutingInfo](docs/RoutingInfo.md)
 - [ScaStatus](docs/ScaStatus.md)
 - [SettlementRequestDTO](docs/SettlementRequestDTO.md)
 - [StakeholderContactDetailsResponseDTO](docs/StakeholderContactDetailsResponseDTO.md)
 - [StakeholderDetails](docs/StakeholderDetails.md)
 - [StakeholderDetails2](docs/StakeholderDetails2.md)
 - [StakeholderDetailsResponseDTO](docs/StakeholderDetailsResponseDTO.md)
 - [StakeholderDetailsV2](docs/StakeholderDetailsV2.md)
 - [StakeholderV2](docs/StakeholderV2.md)
 - [Stakeholders](docs/Stakeholders.md)
 - [Stakeholders2](docs/Stakeholders2.md)
 - [Standard401Error](docs/Standard401Error.md)
 - [Standard403Error](docs/Standard403Error.md)
 - [Standard404Error](docs/Standard404Error.md)
 - [Standard500Error](docs/Standard500Error.md)
 - [SupportedCorridorsResponseDTO](docs/SupportedCorridorsResponseDTO.md)
 - [SupportedCorridorsResponseDTO2](docs/SupportedCorridorsResponseDTO2.md)
 - [TaxDetails](docs/TaxDetails.md)
 - [TaxDetailsResponseDTO](docs/TaxDetailsResponseDTO.md)
 - [Template](docs/Template.md)
 - [TermsAndConditionsAcceptResponseDTO](docs/TermsAndConditionsAcceptResponseDTO.md)
 - [TermsAndConditionsRequestDTO](docs/TermsAndConditionsRequestDTO.md)
 - [TermsAndConditionsResponseDTO](docs/TermsAndConditionsResponseDTO.md)
 - [ThreeDSOOBCallbackRequestDTO](docs/ThreeDSOOBCallbackRequestDTO.md)
 - [Transaction](docs/Transaction.md)
 - [TransactionAmount](docs/TransactionAmount.md)
 - [TransactionChannelResponseDTO](docs/TransactionChannelResponseDTO.md)
 - [TransactionChannelsResponseDTO](docs/TransactionChannelsResponseDTO.md)
 - [TransactionClientTagRequestDTO](docs/TransactionClientTagRequestDTO.md)
 - [TransactionClientTagResponseDTO](docs/TransactionClientTagResponseDTO.md)
 - [TransactionClientTagsRequestDTO](docs/TransactionClientTagsRequestDTO.md)
 - [TransactionClientTagsResponseDTO](docs/TransactionClientTagsResponseDTO.md)
 - [TransactionLimitDTO](docs/TransactionLimitDTO.md)
 - [TransactionLimitsDTO](docs/TransactionLimitsDTO.md)
 - [TransactionResponseDTO](docs/TransactionResponseDTO.md)
 - [TransactionRfiDetailsResponse](docs/TransactionRfiDetailsResponse.md)
 - [TransactionWalletLimitsDTO](docs/TransactionWalletLimitsDTO.md)
 - [TransactionsBusinessDTO](docs/TransactionsBusinessDTO.md)
 - [TransactionsLocationDTO](docs/TransactionsLocationDTO.md)
 - [TransactionsReceiptDTO](docs/TransactionsReceiptDTO.md)
 - [TypedErrorErrorCodes](docs/TypedErrorErrorCodes.md)
 - [URI](docs/URI.md)
 - [URL](docs/URL.md)
 - [UnmaskCardResponseDTO](docs/UnmaskCardResponseDTO.md)
 - [UpdateBeneficiaryRequestDTO](docs/UpdateBeneficiaryRequestDTO.md)
 - [UpdateContactInfoRequestDTO](docs/UpdateContactInfoRequestDTO.md)
 - [UpdateCorporateKybResponseDTO](docs/UpdateCorporateKybResponseDTO.md)
 - [UpdateCustomerDTO](docs/UpdateCustomerDTO.md)
 - [UpdateCustomerResponseDTO](docs/UpdateCustomerResponseDTO.md)
 - [UploadRfiDetailsResponseDto](docs/UploadRfiDetailsResponseDto.md)
 - [UploadRfiDocumentRequestDto](docs/UploadRfiDocumentRequestDto.md)
 - [VirtualAccountResponseDTO](docs/VirtualAccountResponseDTO.md)
 - [WalletApiError](docs/WalletApiError.md)
 - [WalletApiResponse2](docs/WalletApiResponse2.md)
 - [WalletApiResponseOfstring](docs/WalletApiResponseOfstring.md)
 - [WalletBalanceResponseDTO](docs/WalletBalanceResponseDTO.md)
 - [WalletFundDTO](docs/WalletFundDTO.md)
 - [WalletFundResponseDTO](docs/WalletFundResponseDTO.md)
 - [WalletFundingInstrumentsResponseDTO](docs/WalletFundingInstrumentsResponseDTO.md)
 - [WalletPaymentIdsResponseDTO](docs/WalletPaymentIdsResponseDTO.md)
 - [WalletPaymentIdsTagRequestDTO](docs/WalletPaymentIdsTagRequestDTO.md)
 - [WalletPaymentIdsTagRequestDTO2](docs/WalletPaymentIdsTagRequestDTO2.md)
 - [WalletRefundRequestDTO](docs/WalletRefundRequestDTO.md)
 - [WalletRefundResponseDTO](docs/WalletRefundResponseDTO.md)
 - [WalletRfiAttributeResponse](docs/WalletRfiAttributeResponse.md)
 - [WalletRfiResponseRequest](docs/WalletRfiResponseRequest.md)
 - [WalletTransactionsResponseDTO](docs/WalletTransactionsResponseDTO.md)
 - [WalletTransferDto](docs/WalletTransferDto.md)
 - [WalletTransferResponseDto](docs/WalletTransferResponseDto.md)
 - [Window](docs/Window.md)
 - [WithDestinationAmount](docs/WithDestinationAmount.md)
 - [WithDestinationAmount1](docs/WithDestinationAmount1.md)
 - [WithSourceAmount](docs/WithSourceAmount.md)
 - [WithSourceAmount1](docs/WithSourceAmount1.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="default"></a>
### default

- **Type**: API key
- **API key parameter name**: x-api-key
- **Location**: HTTP header


## Author

experience@nium.com


