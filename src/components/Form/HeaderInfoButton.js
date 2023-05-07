import React, { useState } from "react";

import classes from "./HeaderInfoButton.module.css";

const HeaderInfoButton = (props) => {
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
      ⓘ
    </button>
  );
};

export default HeaderInfoButton;
