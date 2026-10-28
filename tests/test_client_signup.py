from pages.client_signup_page import SignupPage


def test_client_signup(driver):

    driver.get("https://dev.my.r3vto.com/account/clientsignup")

    signup = SignupPage(driver)

    signup.enter_card_name("Test User")

    signup.enter_card_details(
        "4242424242424242",
        "04/29",
        "424",
        "42424"
    )

    signup.click_signup()