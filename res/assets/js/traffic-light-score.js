define(['assetman', 'pytsite-widget-select-score', 'font-awesome'], function (assetman, widgetScoreInit) {
    assetman.loadCSS('plugins.widget@css/traffic-light-score.css');

    return function (widget) {
        return widgetScoreInit(widget);
    }
});
