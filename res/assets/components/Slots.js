import './css/Slots.scss';
import React from 'react';
import PropTypes from 'prop-types';


export default class Slots extends React.Component {
    static propTypes = {
        className: PropTypes.string,
        data: PropTypes.object,
        isEmptySlotEnabled: PropTypes.bool,
        maxSlots: PropTypes.number,
        onEmptySlotClick: PropTypes.func,
        renderEmptySlot: PropTypes.func,
        renderSlot: PropTypes.func.isRequired,
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
                <div className={'slot'} key={slotKey}>
                    <div className="inner">
                        {this.props.renderSlot(this.props.data[slotKey])}
                    </div>
                </div>)
            .slice(0, this.props.maxSlots);

        if (this.props.isEmptySlotEnabled && this.props.renderEmptySlot && slots.length < this.props.maxSlots) {
            slots.push(
                <div className={'slot empty'} key={'__empty'} onClick={this.props.onEmptySlotClick}>
                    <div className="inner">
                        {this.props.renderEmptySlot()}
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
        return <div className={`component-widget component-slots ${this.props.className}`}>
            {this.slots}
        </div>;
    }
}
