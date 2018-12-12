import 'select2/dist/css/select2.css';
import 'select2/dist/js/select2';
import 'select2/dist/js/i18n/en';
import 'select2/dist/js/i18n/ru';
import 'select2/dist/js/i18n/uk';
import PropTypes from "prop-types";
import React from 'react';
import $ from 'jquery';


export default class Select2 extends React.Component {
    static propTypes = {
        className: PropTypes.string,
        disabled: PropTypes.bool,
        id: PropTypes.object,
        name: PropTypes.string,
        options: PropTypes.object,
        onReady: PropTypes.func,
        onChange: PropTypes.func,
        onClosing: PropTypes.func,
        onClose: PropTypes.func,
        onOpening: PropTypes.func,
        onOpen: PropTypes.func,
        onSelecting: PropTypes.func,
        onSelect: PropTypes.func,
        onUnselecting: PropTypes.func,
        onUnselect: PropTypes.func,
        userTitleFormat: PropTypes.string,
    };

    static defaultProps = {
        className: 'form-control',
    };

    constructor(props) {
        super(props);
        this.ref = React.createRef();
    }

    componentDidMount() {
        // https://select2.org/configuration/options-api
        const select = $(this.ref.current).select2(this.props.options);

        // See https://select2.org/programmatic-control/events
        select.on('change', this.props.onChange);
        select.on('select2:closing', this.props.onClosing);
        select.on('select2:close', this.props.onClose);
        select.on('select2:opening', this.props.onOpening);
        select.on('select2:open', this.props.onOpen);
        select.on('select2:selecting', this.props.onSelecting);
        select.on('select2:select', this.props.onSelect);
        select.on('select2:unselecting', this.props.onUnselecting);
        select.on('select2:unselect', this.props.onUnselect);

        select.trigger('click');

        this.props.onReady && this.props.onReady(select);
    }

    render() {
        return (
            <select ref={this.ref}
                    id={this.props.id}
                    name={this.props.name}
                    className={this.props.className}
                    disabled={this.props.disabled}>
                {this.props.children}
            </select>
        )
    }
}
