import PropTypes from "prop-types";
import React from 'react';
import {lang} from '@pytsite/assetman';
import {Button, Modal, ModalHeader, ModalBody, ModalFooter} from 'reactstrap';

export default class TwoButtonsModal extends React.Component {
    static propTypes = {
        onToggle: PropTypes.func,
        className: PropTypes.string,
        isOpen: PropTypes.bool,
        okButtonCaption: PropTypes.string,
        isOkButtonDisabled: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
        cancelButtonCaption: PropTypes.string,
        isCancelButtonDisabled: PropTypes.oneOfType([PropTypes.bool, PropTypes.func]),
        onClickCancel: PropTypes.func,
        onClickOk: PropTypes.func,
        title: PropTypes.string,
    };

    static defaultProps = {
        cancelButtonCaption: lang.t('widget@cancel'),
        okButtonCaption: lang.t('widget@ok'),
    };

    constructor(props) {
        super(props);

        this.onClickOk = this.onClickOk.bind(this);
        this.onClickCancel = this.onClickCancel.bind(this);
    }

    onClickOk() {
        this.props.onToggle();
        this.props.onClickOk && this.props.onClickOk();
    }

    onClickCancel() {
        this.props.onToggle();
        this.props.onClickCancel && this.props.onClickCancel();
    }

    render() {
        const isCancelBtnDisabled = this.props.isCancelButtonDisabled instanceof Function ?
            this.props.isCancelButtonDisabled() : this.props.isCancelButtonDisabled;
        const isOkBtnDisabled = this.props.isOkButtonDisabled instanceof Function ?
            this.props.isOkButtonDisabled() : this.props.isOkButtonDisabled;

        return (
            <Modal isOpen={this.props.isOpen} toggle={this.onClickCancel} className={this.props.className}>
                <ModalHeader toggle={this.onClickCancel}>{this.props.title}</ModalHeader>
                <ModalBody>
                    {this.props.children}
                </ModalBody>
                <ModalFooter>
                    <Button color="secondary" disabled={isCancelBtnDisabled} onClick={this.onClickCancel}>
                        {this.props.cancelButtonCaption}
                    </Button>
                    {' '}
                    <Button color="primary" disabled={isOkBtnDisabled} onClick={this.onClickOk}>
                        {this.props.okButtonCaption}
                    </Button>
                </ModalFooter>
            </Modal>
        )
    }
}
