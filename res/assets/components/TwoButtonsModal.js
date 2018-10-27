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
        isOkButtonDisabled: PropTypes.bool,
        cancelButtonCaption: PropTypes.string,
        isCancelButtonDisabled: PropTypes.bool,
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
        return <Modal isOpen={this.props.isOpen} toggle={this.onClickCancel} className={this.props.className}>
            <ModalHeader toggle={this.onClickCancel}>{this.props.title}</ModalHeader>
            <ModalBody>
                {this.props.children}
            </ModalBody>
            <ModalFooter>
                <Button color="secondary" disabled={this.props.isCancelButtonDisabled} onClick={this.onClickCancel}>
                    {this.props.cancelButtonCaption}
                </Button>
                {' '}
                <Button color="primary" disabled={this.props.isOkButtonDisabled} onClick={this.onClickOk}>
                    {this.props.okButtonCaption}
                </Button>
            </ModalFooter>
        </Modal>
    }
}
