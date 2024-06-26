import React, { useState } from "react";

import classes from "./HeaderSettingsButton.module.css";

const HeaderSettingsButton = (props) => {
  const [btnIsHighlighted] = useState(false);

  const btnClasses = `${classes.button} ${
    btnIsHighlighted ? classes.bump : ""
  }`;

  return (
    <button className={btnClasses} onClick={props.onClick}>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      ⚙
    </button>
  );
};

export default HeaderSettingsButton;
