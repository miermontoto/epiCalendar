import React, { useState, useEffect, useContext } from "react";

import classes from "./Checkboxes.module.css";
import SettingsContext from "../../store/settings-context";

// Component that represents the 3 checkboxes
const Checkboxes = () => {
  // Access the settings context
  const ctx = useContext(SettingsContext);

  // Function that handles the checkbox change for location
  const parseHandler = () => {
    ctx.parseHandler(!ctx.parse);
    ctx.updateHandler(true);
  };

  // Function that handles the checkbox change for class type
  const classParsingHandler = () => {
    ctx.classParsingHandler(!ctx.classParsing);
    ctx.updateHandler(true);
  };

  // Function that handles the checkbox change for links
  const linksHandler = () => {
    ctx.linksHandler(!ctx.links);
    ctx.updateHandler(true);
  };

  return (
    <div className={classes.overall}>
      <div>
        <input
          type="checkbox"
          id="location-parsing"
          // checked={parse.parse}
          checked={ctx.parse}
          onChange={parseHandler}
        />
        <label htmlFor="location-parsing">Filtrado de nombres de aulas (solo EPI Gijón)</label>
      </div>
      <div>
        <input
          type="checkbox"
          id="class-parsing"
          // checked={classParse.classParsing}
          checked={ctx.classParsing}
          onChange={classParsingHandler}
        />
        <label htmlFor="class-parsing">Filtrado de tipo de clases</label>
      </div>
      <div>
        <input
          type="checkbox"
          id="links"
          // checked={classParse.classParsing}
          checked={ctx.links}
          onChange={linksHandler}
        />
        <label htmlFor="links">Añadir enlaces de ubicación en la descripción</label>
      </div>
    </div>
  );
};

export default Checkboxes;
