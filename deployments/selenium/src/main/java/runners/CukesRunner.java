package runners;

import cucumber.api.CucumberOptions;
import cucumber.api.junit.Cucumber;
import org.junit.AfterClass;
import org.junit.runner.RunWith;

@RunWith(Cucumber.class)
@CucumberOptions(
        plugin = {"html:target/cucumber-reports",

                "json:target/cukesreport.json"},
        features = "src/test/resources/features/",
        glue = "step_definitions",
        dryRun = false,
        tags = "@wiki"

)

public class CukesRunner {


}
