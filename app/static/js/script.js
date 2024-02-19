///////////////////////////////////////////////
// Object 1: User Input


///////////////////////////////////////////////
// Object 2: Input/Log Format
// The function selects the clicked button and checks the corresponding radio input for *Log Format* in Object 2
// it is called from the corresponding button in the HTML file with "onclick" attribute
function selectFormat(value, group) {
    // Deselect all buttons in the group and select the clicked one
    document.querySelectorAll('.' + group).forEach(btn => btn.classList.remove('selected'));
    document.getElementById(value).classList.add('selected');
    document.getElementById(value + '_radio').checked = true; // Check the corresponding radio input
}

/////////////////////////////////////////////
// Objects 3 and 4: Taper Distribution and Log Options

// Deselects all log option buttons associated with the Taper Distribution options
function selectLogOption(logType, optionValue) {
    // Prefix for button and radio IDs
    const prefix = logType + '_' + optionValue;

    // Deselect all buttons and uncheck all radios in the same group
    document.querySelectorAll('.' + logType + '-log-btn').forEach(button => {
        button.classList.remove('selected'); 
    });
    document.querySelectorAll('input[name="' + logType + '_log_option"]').forEach(radio => {
        radio.checked = false;
    });

    // Select the clicked button and check the corresponding radio input
    document.getElementById(prefix + '_btn').classList.add('selected');
    document.getElementById(prefix + '_radio').checked = true;
}


function presetSelections(group, option) {
    // Preset a specific button as selected and check its radio button in Object 4
    const buttonId = `${group}_${option}_btn`;
    const radioId = `${group}_${option}_radio`;
    document.getElementById(buttonId).classList.add('selected');
    document.getElementById(radioId).checked = true;
}


function selectTaperOption(selectedOption) {
    // Reset Object 4 and Object 3 to default state
    resetObject4();
    resetObject3();

    // Select the clicked button and check the corresponding radio input in Object 3
    document.getElementById(selectedOption + '_btn').classList.add('selected');
    document.getElementById(selectedOption + '_radio').checked = true;

    // Apply logic based on the selection in Object 3
    switch (selectedOption) {
        case 'lambert':
            // Apply 'selected' class to preset buttons for Lambert
            document.getElementById('butt_5_6_btn').classList.add('selected');
            document.getElementById('middle_3_4_btn').classList.add('selected');
            document.getElementById('top_1_2_btn').classList.add('selected');

            // Lock all buttons in Object 4
            lockGroup('butt-log', true);
            lockGroup('middle-log', true);
            lockGroup('top-log', true);
            break;
        case 'true_taper':
            // Enable only "butt-log" buttons, keep others locked
            lockGroup('middle-log', true);
            lockGroup('top-log', true);
            break;
        case 'custom':
            // Unlock all buttons in Object 4
            lockGroup('butt-log', false);
            lockGroup('middle-log', false);
            lockGroup('top-log', false);
            break;
    }
}
 
///////////////////////////////////////////////
// Helper Functions
// lockGroup function locks or unlocks all buttons in a specific group in Object when called
function lockGroup(groupID, lock) {
    // Lock or unlock all buttons in a specific group in Object 4
    const buttons = document.querySelectorAll(`#${groupID} button`);
    buttons.forEach(button => button.disabled = lock);
}

function resetObject3() {
    // Deselect all buttons and uncheck all radio inputs in Object 3
    document.querySelectorAll('.taper-btn').forEach(button => button.classList.remove('selected'));
    document.querySelectorAll('input[name="taper_option"]').forEach(radio => radio.checked = false);
}


function resetObject4() {
    // Remove 'selected' class from all buttons, enable them, and uncheck all radio inputs in Object 4
    document.querySelectorAll('.object .taper-option button').forEach(button => {
        button.classList.remove('selected');
        button.disabled = false;
    });
    document.querySelectorAll('.object .taper-option input[type="radio"]').forEach(radio => radio.checked = false);
}

///////////////////////////////////////////////
// Bindings
// Add event listeners to buttons in Object 3
document.getElementById('lambert_btn').addEventListener('click', () => selectTaperOption('lambert'));
document.getElementById('true_taper_btn').addEventListener('click', () => selectTaperOption('true_taper'));
document.getElementById('custom_btn').addEventListener('click', () => selectTaperOption('custom'));
