/* Page initialization logic */
window.addEventListener("load", function() {
  const heatmapForm = document.getElementById("heatmap-form");

  heatmapForm.addEventListener("submit", function(event) {
    // Prevent full page form submission and just send the api call
    event.preventDefault();
    hideError();
    toggleLoading(true);
    // Get the input from the form
    const formData = new FormData(heatmapForm);
    // Set default values
    // Checkboxes do not submit a value when not checked
    if (!formData.get('in_scoring_pos')) {
      formData.set('in_scoring_pos', 'False');
    }
    if (!formData.get('on_base')) {
      formData.set('on_base', 'False');
    }

    // Delete pitch type if default option is selected
    if (formData.get('pitch_type') === 'null') {
      formData.delete('pitch_type');
    }

    // Coerce location radio button into boolean
    if (formData.get('location') === 'home') {
      formData.set('home', 'True');
    } else {
      formData.set('home', 'False');
    }
    formData.delete('location');
    
    return generateHeatmap(formData)
      .then(heatmap => {
        toggleLoading(false);
        drawHeatmap(heatmap);
      })
      .catch(error => {
        toggleLoading(false);
        showError(error.message);
      });
  });

  const batterInput = document.getElementById("batter");
  configureTypeahead("batters", batterInput);
  showPlayerHandednessIfNeeded(batterInput, "stance");
  const pitcherInput = document.getElementById("pitcher");
  configureTypeahead("pitchers", pitcherInput);
  showPlayerHandednessIfNeeded(pitcherInput, "throws");
});

/* Drawing/rendering logic */
function toggleLoading(isLoading) {
  const loadingIndicator = d3.select("#loading-indicator");
  loadingIndicator.classed("hidden", !isLoading);
}

function showError(message) {
  const errorNode = d3.select("#error-message");

  if (errorNode.classed("hidden")) {
    errorNode.classed("hidden", false);
  }

  errorNode.text(message);
}

function hideError() {
  d3.select("#error-message").classed("hidden", true);
}

/**
 * Adds a listener for typeahead 
 * @param {string} playerType The type of player to search. Valid values are "batters" and "pitchers".
 * @param {HTMLInputElement} inputElement A text input.
 */
function configureTypeahead(playerType, inputElement) {
  const listElement = document.getElementById(inputElement.getAttribute("list"));
  inputElement.addEventListener("input", function(event) {
    const data = event.target.value;
    const minimumLengthForTypeahead = 3;
    if (data && data.length === minimumLengthForTypeahead) {
      getPlayerTypeaheadSuggestions(playerType, data).then(function(players) {
        while (listElement.hasChildNodes()) {
          listElement.removeChild(listElement.lastChild);
        }
        players.forEach(function(player) {
          const optionNode = document.createElement("option");
          optionNode.setAttribute("data-value", player.id);
          optionNode.setAttribute("label", `${player.position}, ${player.team_short}`);
          optionNode.innerText = player.name;
          listElement.appendChild(optionNode);
        });
      });
    }
  });
}

function showPlayerHandednessIfNeeded(playerNameInputElement, handednessQualityName) {
  playerNameInputElement.addEventListener("blur", function (event) {
    const container = d3.select(`.input-container.${handednessQualityName}`);
    if (!event.target.value) {
      if (container.classed("hidden")) {
        container.classed("hidden", false);
      }
      // Enable previously disabled inputs and give the first one focus
      container.selectAll("input")
        .property("disabled", false)
        .node()
        .focus();
    } else {
      container.classed("hidden", true);
      // Disabled inputs
      container.selectAll("input")
        .property("disabled", true);
      // TODO: force the browser focus to the next element in the form
    }
  });
}

/**
 * An object describing a heatmap. Zone provides the coordinates of the strike zone
 * in the form [x1, y1, x2, y2] where (x1, y1) is the bottom-left corner and (x2, y2)
 * is the top-right corner of a rectangle. Each of x, y, and heat are an ordered set
 * of data points to be mapped at (x, y) with a value of heat.
 * @typedef {{ zone: number[], x: number[], y: number[], heat: number[] }} Heatmap
 */

/**
 *
 * @param {Heatmap} heatmap An object containing heatmap data
 */
function drawHeatmap(heatmap) {
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
  // Calculate the dimensions and placement of the strike zone
  const strikeZone = {
    width: heatmap.zone[2] - heatmap.zone[0],
    height: heatmap.zone[3] - heatmap.zone[1],
    xOffset: heatmap.zone[0] - boundingBox[0].x,
    yOffset: boundingBox[1].y - heatmap.zone[3]
  };

  // The svg coordinate system places (0,0) in the top-left corner
  // While our coordinate system places (0,0) in the center of the bottom
  const boundingBoxOrigin = {
    x: boundingBoxWidth / 2,
    y: boundingBoxHeight
  };

  // Process the raw heatmap data
  const data = [];
  for (let index = 0; index < heatmap.x.length; index++) {
    const x = heatmap.x[index];
    const y = heatmap.y[index];
    const heat = heatmap.heat[index];
    data.push({
      ...transformCoordinates(x, y, boundingBoxOrigin, scale),
      heat
    });
  }

  // Render the heat points
  const svg = d3.select("svg#visualization");

  svg
    .attr("width", boundingBoxWidth * scale)
    .attr("height", boundingBoxHeight * scale)
    .select("g#heatmap")
    .selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => d.x)
    .attr("y", d => d.y)
    .attr("width", pointWidth * scale)
    .attr("height", pointHeight * scale)
    .attr("fill", d => getColor(d.heat))
    .attr("stroke", d => getColor(d.heat));

  // Render the strike zone
  svg
    .select("g#strikezone")
    .selectAll("rect")
    .data([strikeZone])
    .join("rect")
    .attr("x", strikeZone => strikeZone.xOffset * scale)
    .attr("y", strikeZone => strikeZone.yOffset * scale)
    .attr("width", strikeZone => strikeZone.width * scale)
    .attr("height", strikeZone => strikeZone.height * scale)
    .attr("stroke", "black")
    .attr("fill", "none");
}

/**
 * Produce a color for the given heat value for display. See
 * https://github.com/d3/d3-scale-chromatic/tree/v1.5.0#interpolateRdYlGn
 * @param {number} heat A number between 0 and 1
 */
function getColor(heat) {
  const colorScale = d3.scaleSequential(d3.interpolateRdYlBu).domain([0, 0.5]);
  return colorScale(0.5 - heat);
}

/**
 * Transform raw coordinates to match the scale and dimensions of the render area.
 * @param {number} x The x coordinate of a point.
 * @param {number} y The y coordinate of a point.
 * @param {{ x: number, y: number }} origin The origin of the new coordinate system.
 * @param {number} scale The scale factor of the new coordinate system.
 */
function transformCoordinates(x, y, origin, scale) {
  const remappedX = x + origin.x;
  // The svg coordinate system has the positive y-axis extending down
  const remappedY = origin.y - y;
  // Finally, scale
  return {
    x: remappedX * scale,
    y: remappedY * scale
  };
}

/* API Calls */

/**
 * Makes a request to the API, returning the JSON response.
 * @param {string} endpointUrl The API endpoint that is the destination of the request.
 * @param {any} options Request options. Same as fetch options but with params for query parameters.
 */
function makeJsonRequest(endpointUrl, options) {
  const baseUrl = window.location.href; // server host
  const url = new URL(endpointUrl, baseUrl);
  if (options.params) {
    const urlParams = new URLSearchParams(options.params);
    url.search = urlParams.toString();
  }
  return fetch(url, { method: options.method, body: options.body }).then(
    function(response) {
      if (response.ok) {
        return response.json();
      }
      throw new Error(
        `Api responded with status code: ${response.status} error: ${response.statusText}`
      );
    }
  );
}

/**
 * Generate a heatmap for the given form input.
 * @returns {Promise<Heatmap>}
 */
function generateHeatmap(formData) {
  return makeJsonRequest("/heatmap", { method: "POST", body: formData });
}

/**
 * Get player typeahead suggestions.
 * @param {string} playerType The type of player to search. Valid values are "batters" and "pitchers". 
 * @param {string} namePrefix The prefix to match for suggestions.
 */
function getPlayerTypeaheadSuggestions(playerType, namePrefix) {
  const params = { name_prefix: namePrefix };
  return makeJsonRequest(`/${playerType}`, { method: "GET", params });
}
