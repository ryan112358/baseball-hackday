import * as d3 from "d3";
import data from "../../heatmap.json";

// The bottom-left and top-right coordinates of the total area we'll be charting
const boundingBox = [
  { x: -2, y: 0 },
  { x: 2, y: 5 }
];
// A scalar value applied to all coordinates to render the image large enough to see clearly
const scale = 100;

// Calculate the dimensions of the bounding box
const boundingBoxWidth = boundingBox[1].x - boundingBox[0].x;
const boundingBoxHeight = boundingBox[1].y - boundingBox[0].y;
// Calculate the dimensions of the strike zone
const strikeZoneWidth = data.zone[2] - data.zone[0];
const strikeZoneHeight = data.zone[3] - data.zone[1];
// Calculate the placement of the strike zone within the bounding box
const strikeZoneXOffset = data.zone[0] - boundingBox[0].x;
const strikeZoneYOffset = boundingBox[1].y - data.zone[3];

// Render the visualization
d3.select("#root")
  .append("svg")
  .attr("width", boundingBoxWidth * scale)
  .attr("height", boundingBoxHeight * scale)
  .call(svg =>
    svg
      .append("rect")
      .style("stroke", "black")
      .style("fill", "none")
      .attr("x", strikeZoneXOffset * scale)
      .attr("y", strikeZoneYOffset * scale)
      .attr("width", strikeZoneWidth * scale)
      .attr("height", strikeZoneHeight * scale)
  );
