$(document).ready(function() {
    // TODO: Create an internal flask api to set a color mode session variable
    // We can then use the session variable to keep toggle consistent throughout the user's session.
    $('#color_mode_toggle').change(function() {
        if (this.checked) {
            document.documentElement.setAttribute('color-mode', 'dark');
        }
        else {
            document.documentElement.setAttribute('color-mode', 'light');
        }
    });
});
