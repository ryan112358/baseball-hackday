# baseball-hackday

## Rendering the visualization

The json data and javascript source code are compiled into a single artifact and injected into an html document during a webpack build process. Thus, the following steps are required to view the visualization of the data:

1. Install the latest version of Node.js from https://nodejs.org/en/download/
2. From the `visualization/` directory, run `npm install` to download the project dependencies (build tools & d3.js).
3. Run the build process with `npm run build`
4. Open `visualization/dist/index.html` in a web browser.
5. Alternatively, run `npm run dev` to build and serve the visualization in development mode. This allows changes to the source code to trigger a rebuild and be hot reloaded into the browser. View the visualization at http://localhost:8080.
