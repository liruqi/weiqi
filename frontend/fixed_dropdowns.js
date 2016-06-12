// This fixes dropdowns which appear inside an `overflow: auto` container with fixed width/height.
// Without this a dropdown would be clipped at the borders of the containers instead of appearing on top of it.
// Drawback is that scrolling will not scroll the dropdown-menu and there is no easy way to emulate it as the `scroll`
// event does not buble and is not supported for delegation in jQuery:
//   $('body').on('scroll', '.fixed-dropdowns', ... // will not work
export function fix_dropdowns() {
    jQuery('body').on('click', '.fixed-dropdowns .dropdown-toggle', function () {
        var button = jQuery(this);
        var dropdown_menu = button.next();
        var top = button.offset().top + button.outerHeight();
        
        dropdown_menu.css('position', 'fixed');
        dropdown_menu.css('top', top + "px");
        dropdown_menu.css('left', button.offset().left + "px");
    });
}
