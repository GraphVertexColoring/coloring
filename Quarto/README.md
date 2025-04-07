## structure ideas
Can use a listing page for the analysis, ensuring that their titles hopefuly can be generated dynamically enough that they become identifiable.
    Adding the date time will function aswell for sorting purposes.
    Author of the the requested analysis could be used aswell, this can simply be added to the config for creating ISA.
    Can reuse old code for plotting should add small modifications to make it more suited for the current format though.
        Still need to see if the explanations for the features look terrible here or not?

    Must modify the config used to ensure that the new needed values are added.
    Should find simple way to modify title, date and name, to allow for simple generation of analysis pages.

the about page has a default structure that i will be using.

the sidebar looks cleaner than the navbar.

The best known table could be done using lists similar to listings maybe, and then have some sub ones that contain the individual s,m,d and ? lists.

## Publishing on pages
Should add the _sites and .quarto to a .gitignore as these shouldnt be pushed to version control.

To publish, make a seperate branch, and then use the quarto publish command.
        quarto publish gh-pages
The command above should work fine.

or follow the github actions guide found on quarto.

Before setting up the action the publish command should be run manually atleast once, this is to ensure that the _publish.yaml is created.
An example action is present in githubActionPublish.yaml   
        Could maybe modify it to also take care of the execution of the ISA in the same action?

For custom site domain, use a CNAME file.


## Actions

for feature extraction i can have the code run from in the ISA repo and extract features, the trigger should be placed in the data.archive repo and simply call the extraction action.

Similar thing can be done for the performance extraction.

For the ISA, a push to the ISA could simply trigger there or maybe even trigger an action from the publishing repo, which then pulls the 3 needed files from the ISA repo, and generates the qmd, before deleting the analysis files that are no longer needed. then pushes the changes and republish the page.

The potential IOH focused actions could work similarly, to the ISA ones where the work is performed to generate some page, and then the site is re rendered and published.

maybe the publishing action could be reused by simply having it trigger when the ISA/IOH do a push to the pages repo.