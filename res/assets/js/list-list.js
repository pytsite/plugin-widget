define(['assetman', 'widget-input-string-list'], function(assetman, stringList) {
    assetman.loadCSS('plugins.widget@css/list-list.css');

    return function(widget) {
        stringList(widget);
    }
});
