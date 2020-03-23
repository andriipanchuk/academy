package tests;

import com.github.javafaker.Faker;
import org.junit.Test;
import pages.SignUp_page;
import utilities.Config;
import utilities.Driver;

public class Signup {
    SignUp_page signUp_page = new SignUp_page();

    @Test
    public void setUp() throws Exception {
        Faker faker = new Faker();
        Driver.getDriver().get(Config.getProperty("academyURL"));
        signUp_page.signUpTodayButton.click();

        Thread.sleep(1000);
        signUp_page.firstNameInputBox.sendKeys(faker.name().firstName());
        Thread.sleep(1000);
        signUp_page.lastNameInputBox.sendKeys(faker.name().lastName());
        Thread.sleep(1000);
        signUp_page.usernameInputBox.sendKeys(faker.name().username());
        Thread.sleep(1000);
        signUp_page.emailInputBox.sendKeys("Uusernamee@gmail.com");
        signUp_page.passwordInputBox.sendKeys("AAdmin12345123r");
        signUp_page.signUpButton.click();

    }

}
