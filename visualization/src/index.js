import data from "../../heatmap.json";

d3.select("#root")
  .selectAll("p")
  .data(data.zone)
  .enter()
  .append("p")
  .text(function(d) {
    return "I’m number " + d + "!";
  });
