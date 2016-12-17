#Data Visualization of Titanic Survival Rates with Dimple and D3 JS
**_Completed by Michael Ochs for Udacity Data Analytics Nanodegree_**

##Summary
The data visualization in this project illustrates the survival rate of passengers of the Titanic.  The survival rates are separated by class then gender.  The purpose of the visualization is to give a brief yet deeper look into who had the greatest and least chance of survival.  Upon inspection, it's clear that females in first class had the highest chance of survival and men in third class had the least chance of survival.

##Design

![alt tag](https://github.com/mtochs/Udacity/Data%20Analytics%20Nanodegree/P6%20Data%20Visualization%20with%20Dimple%20and%20D3%20JS/py_chart.png "Original chart from ipython notebook")

##Feedback
- **Colors**: One feedback mentioned that the colors are confusing and counterintuitive.  It's more commonly seen that male color is blue and female color is pink.  The pink might be too much of a contrast.  By default, male color was red and female color was blue.  Thus, the colors of red and blue were switched. 

- **Opacity**: Version 2 of the graph had an opacity setting of 1.  This correlates to no transparency.  Observes did not like it.  The complaint was that it made it harder to see where the bar chart fits against the axis.  Opacity was later adjusted to .7 (or 70%).

- **Age**: A suggestion was to split the data by age.  This suggestion was declined since it would add more clutter to the visualization.  As a result, it might take away from the emphasis that class had on survival.  Furthermore, there was a relatively small number of children in the data. Of the total 891 data points, 177 did not have age and 133 were less than 18 (i.e. 17 or younger).  In other words, only 12.7% of the data was of children. 

- **Data Order**: The first version did not have the classes in numerical order.  Class should be shown sequentially as 1, 2, 3.  In version 1 it was displayed as 1, 3, 2.  This critique was used to update the visualization to provide a clearer understanding on how passenger class correlated to survival rate.

- **Axis Titles**: The first versions did not have any titles.  It was suggested that the x and y axis are renamed to more intuitive names.  It was also recommended to create a title for the overall visualization.

##Resources
Data visualization framework provided by:
http://dimplejs.org/examples_viewer.html?id=bars_vertical_grouped

Huge thank you to Myles Callan!!  Myles timeliness and thorough responses on the Udacity forum have been a huge help and guide in completing this project.
https://discussions.udacity.com/t/final-project-start/203226