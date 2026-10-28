from pages.customer_page import CustomerPage



def test_add_customer(driver, excel_data):

    data_rows = excel_data.get_sheet_data("ExCert_Customers")

    customer_page = CustomerPage(driver)

    for row in data_rows:
        customer_page.navigate_to_excert_manager()
        customer_page.navigate_to_sales()
        customer_page.navigate_to_customers()

        customer_page.click_add_customer()

        customer_page.fill_customer_form(row)
        customer_page.submit_form()

        print(f"Successfully added customer: {row['CustomerName']}")