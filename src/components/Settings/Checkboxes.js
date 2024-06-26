import React, { useContext } from "react";

import classes from "./Checkboxes.module.css";
import SettingsContext from "../../store/settings-context";

// Component that represents the 3 checkboxes
const Checkboxes = () => {
  // Access the settings context
  const ctx = useContext(SettingsContext);

  // State for the checkboxes
  // const [parse, setParse] = useState({ parse: true, parseDisabled: false });
  // const [classParse, setClassParse] = useState({
  //   classParsing: true,
  //   classParsingDisabled: false,
  // });

  // No dependecies as we want the checkboxes to be updated only on first render
  // useEffect(() => {
  //   if (ctx.university === "uo") {
  //     setParse({
  //       parse: ctx.oviedoCheck.parse,
  //       parseDisabled: ctx.oviedoCheck.parseDisabled,
  //     });
  //     setClassParse({
  //       classParsing: ctx.oviedoCheck.classParsing,
  //       classParsingDisabled: ctx.oviedoCheck.classParsingDisabled,
  //     });
  //   } else if (ctx.university === "epi") {
  //     setParse({
  //       parse: ctx.epiCheck.parse,
  //       parseDisabled: ctx.epiCheck.parseDisabled,
  //     });
  //     setClassParse({
  //       classParsing: ctx.epiCheck.classParsing,
  //       classParsingDisabled: ctx.epiCheck.classParsingDisabled,
  //     });
  //   }
  // }, [ctx.university, ctx.update]);

  // // Effect for updating the checkboxes
  // useEffect(() => {
  //   ctx.parseHandler(parse.parse);
  //   ctx.classParsingHandler(classParse.classParsing);
  // }, [parse.parse, classParse.classParsing]);

  // Function that handles the checkbox change (parse or location)
  const parseHandler = () => {
    ctx.parseHandler(!ctx.parse);
    ctx.updateHandler(true);
  };

  // Function that handles the checkbox change (class-type or class-type)
  const classParsingHandler = () => {
    ctx.classParsingHandler(!ctx.classParsing);
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
        <label htmlFor="location-parsing">Location parsing (recommended for EPI Gijón)</label>
      </div>
      <div>
        <input
          type="checkbox"
          id="class-parsing"
          // checked={classParse.classParsing}
          checked={ctx.classParsing}
          onChange={classParsingHandler}
        />
        <label htmlFor="class-parsing">Class type parsing</label>
      </div>
    </div>
  );
};

export default Checkboxes;
