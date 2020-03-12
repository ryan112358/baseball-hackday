import * as d3 from "d3";
import heatmap from "../../heatmap.json";

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
// Calculate the dimensions of a single point on the heatmap
// TODO: reliably calculate these dimensions from the data
const pointWidth = boundingBoxWidth / 50;
const pointHeight = boundingBoxHeight / 50;
// Calculate the dimensions of the strike zone
const strikeZoneWidth = heatmap.zone[2] - heatmap.zone[0];
const strikeZoneHeight = heatmap.zone[3] - heatmap.zone[1];
// Calculate the placement of the strike zone within the bounding box
const strikeZoneXOffset = heatmap.zone[0] - boundingBox[0].x;
const strikeZoneYOffset = boundingBox[1].y - heatmap.zone[3];

/**
 * Produce a color for the given heat value for display. See
 * https://github.com/d3/d3-scale-chromatic/tree/v1.5.0#interpolateRdYlGn
 * @param {number} heat A number between 0 and 1
 */
function getColor(heat) {
  return d3.interpolateRdYlBu(1 - heat);
}

/**
 * Transform raw coordinates to match the scale and dimensions of the render area.
 * @param {number} x The x coordinate of a point.
 * @param {number} y The y coordinate of a point.
 */
function transformCoordinates(x, y) {
  // The svg coordinate system places (0,0) in the top-left corner
  // While our coordinate system places (0,0) in the center of the bottom
  const boundingBoxOrigin = {
    x: boundingBoxWidth / 2,
    y: boundingBoxHeight
  };
  const remappedX = x + boundingBoxOrigin.x;
  // The svg coordinate system has the positive y-axis extending down
  const remappedY = boundingBoxOrigin.y - y;
  // Finally, scale
  return {
    x: remappedX * scale,
    y: remappedY * scale
  };
}

// Process the raw heatmap data
const data = [];
for (let index = 0; index < heatmap.x.length; index++) {
  const x = heatmap.x[index];
  const y = heatmap.y[index];
  const heat = heatmap.heat[index];
  data.push({ ...transformCoordinates(x, y), heat });
}

// Render the heat points
d3.select("#root")
  .append("svg")
  .attr("id", "boundingBox")
  .attr("width", boundingBoxWidth * scale)
  .attr("height", boundingBoxHeight * scale)
  .selectAll("rect")
  .data(data)
  .join("rect")
  .attr("x", d => d.x)
  .attr("y", d => d.y)
  .attr("width", Math.ceil(pointWidth * scale))
  .attr("height", Math.ceil(pointHeight * scale))
  .attr("fill", d => getColor(d.heat))
  .attr("stroke", d => getColor(d.heat));

// Render the strike zone
d3.select("#boundingBox")
  .append("rect")
  .style("stroke", "black")
  .style("fill", "none")
  .attr("x", strikeZoneXOffset * scale)
  .attr("y", strikeZoneYOffset * scale)
  .attr("width", strikeZoneWidth * scale)
  .attr("height", strikeZoneHeight * scale);
