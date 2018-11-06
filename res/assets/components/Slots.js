import './css/Slots.scss';
import React from 'react';
import PropTypes from 'prop-types';

export default class Slots extends React.Component {
    static propTypes = {
        slotRenderer: PropTypes.func.isRequired,
        className: PropTypes.string,
        data: PropTypes.object,
        enabled: PropTypes.bool,
        maxSlots: PropTypes.number,
        onEmptySlotClick: PropTypes.func,
        onSlotClick: PropTypes.func,
        emptySlotRenderer: PropTypes.func,
    };

    static defaultProps = {
        className: '',
    };

    /**
     * Constructor
     *
     * @constructor
     * @param {Object} props
     */
    constructor(props) {
        super(props);
    }

    /**
     * Get slots
     *
     * @returns {Array}
     */
    get slots() {
        const slots = Object.keys(this.props.data)
            .map(slotKey =>
                <div className={'slot'} key={slotKey} onClick={() => this.props.onSlotClick && this.props.onSlotClick(slotKey)}>
                    <div className="inner">
                        {this.props.slotRenderer(this.props.data[slotKey])}
                    </div>
                </div>)
            .slice(0, this.props.maxSlots);

        if (this.props.enabled && this.props.emptySlotRenderer && slots.length < this.props.maxSlots) {
            slots.push(
                <div className={'slot empty'} key={'__empty'} onClick={this.props.onEmptySlotClick}>
                    <div className="inner">
                        {this.props.emptySlotRenderer()}
                    </div>
                </div>
            );
        }

        return slots;
    }

    /**
     * Render the component
     *
     * @returns {React.Component}
     */
    render() {
        return (
            <div className={`component-widget component-slots ${this.props.className}`.trim()}>
                {this.slots}
            </div>
        );
    }
}
