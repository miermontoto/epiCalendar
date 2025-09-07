import React, { createContext, useState, useMemo } from "react";

// Default values for the context
export const DEFAULT_FILENAME = "Calendario";

// Context for the settings of the app (better autocomplete)
const SettingsContext = createContext({

	saveNameHandler: (name) => {},
	saveas: "",
	parse: false,
	parseHandler: (state) => {},
	classParsing: true,
	classParsingHandler: (state) => {},
	update: false,
	updateHandler: (state) => {},
	extension: ".ics",
	extensionHandler: (extension) => {},
});

export const SettingsProvider = (props) => {
	const [saveas, setSaveas] = useState("Calendario"); // State for the filename

	// States for checkboxes
	const [update, setUpdate] = useState(false);
	const [isCheckedParsing, setIsCheckedParsing] = useState(false);
	const [isClassParsing, setIsClassParsing] = useState(true);

	// State for the extension of the file
	const [extension, setExtension] = useState(".ics");

	const settingsValue = useMemo(() => {
		// Function to set the filename state
		const saveNameHandler = (name) => {
			setSaveas(name);
		};

		// Functions to set the checkboxes state
		const parseHandler = (state) => {
			setIsCheckedParsing(state);
		};
		const classParsingHandler = (state) => {
			setIsClassParsing(state);
		};

		// Function to set the update state
		const updateHandler = (state) => {
			setUpdate(state);
		};

		// Function to set the extension state
		const extensionHandler = (extension) => {
			setExtension(extension);
		};

		return {
			saveNameHandler,
			saveas,
			parseHandler,
			parse: isCheckedParsing,
			classParsing: isClassParsing,
			classParsingHandler,
			update,
			updateHandler,
			extension,
			extensionHandler,
		};
	}, [saveas, isCheckedParsing, isClassParsing, update, extension]);

	return (
		<SettingsContext.Provider value={settingsValue}>
		{props.children}
		</SettingsContext.Provider>
	);
};

export default SettingsContext;
