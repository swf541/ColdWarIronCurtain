# HoI4-Scripted-GUI-Pie-Chart
An example way of how to implement a Scripted GUI pie chart in Hearts of Iron 4.

![Showcase GIF](https://thumbs.gfycat.com/UnnaturalInconsequentialEsok-size_restricted.gif)

A pie segment iconType equivalent to a 1/100 of the entire pie is created 100 times, each time with a 3.6 degree rotation, creating a full pie in the end. The texture contains frames - and which frame is shown is controlled by a 100 element `pie_chart` array, with each element corresponding to an iconType. The `create_pie_chart` scripted effect is used to create the `pie_chart` array, updating the pie chart. In this example, it is called daily.

The pie chart can be easily resized with `scale` argument in the .gui file. Changing the number of possible colors is also easy - one just needs to add/remove frames from the `gfx/interface/pie_chart_segment.dds` texture, and update the .gfx entry and the `create_pie_chart` scripted effect. This pie chart can be used to represent any values adding up to 100% - in this example, vanilla party popularities are used.

You may overlay a pie chart overlay onto this pie chart, to make it look nicer.

Feel free to use in your mods, but give credits to Yard1 (both in code, with comments; and on your download page).