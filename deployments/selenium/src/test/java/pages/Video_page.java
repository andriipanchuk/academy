package pages;

import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import utilities.Driver;

import java.util.List;

public class Video_page {

    public Video_page(){
        PageFactory.initElements(Driver.getDriver(), this);
    }
    @FindBy(xpath = "//span[@style='font-size:30px;cursor:pointer']")
    public WebElement menuButton;

    @FindBy(xpath = "(//div[@id='mySidenav']//a)[4]")
    public WebElement videoButton;

    @FindBy(xpath = "(//div[@class='vertical-menu'])")
    public List<WebElement> videos;

    @FindBy(xpath = "/html/body/div[3]/a")
    public List<WebElement>  itemFromList;

}
