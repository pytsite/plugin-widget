import '../css/tree-table.scss';
import httpApi from '@pytsite/http-api';
import setupWidget from '@pytsite/widget';
import PropTypes from 'prop-types';
import React from 'react';
import ReactDOM from 'react-dom';
import {DragDropContext, Droppable, Draggable} from 'react-beautiful-dnd';
import {Table} from 'reactstrap';


class Row extends React.Component {
    static propTypes = {
        className: PropTypes.string,
        fields: PropTypes.arrayOf(PropTypes.string).isRequired,
        fieldsTitles: PropTypes.object.isRequired,
        hasChildren: PropTypes.bool.isRequired,
        index: PropTypes.number.isRequired,
        onCollapseClick: PropTypes.func,
        onExpandClick: PropTypes.func,
        rowData: PropTypes.object.isRequired,
    };

    static defaultProps = {
        className: '',
    };

    constructor(props) {
        super(props);

        this.onExpanderClick = this.onExpanderClick.bind(this);
    }

    onExpanderClick() {
        if (this.props.rowData.__collapsed)
            this.props.onExpandClick && this.props.onExpandClick(this.props.rowData.__id);
        else
            this.props.onCollapseClick && this.props.onCollapseClick(this.props.rowData.__id);
    }

    render() {
        const row = this.props.rowData;

        let className = this.props.className + ` depth-${row.__depth}`;
        className += this.props.hasChildren ? ' has-children' : '';
        className += row.__collapsed ? ' is-collapsed' : ' is-expanded';

        if (row.__hidden)
            className += ' is-hidden';

        return <Draggable draggableId={row.__id} index={this.props.index}>
            {(provided, snapshot) => {
                // TDs array
                const tds = [];

                // Drag handle and expander
                tds.push(
                    <td key={'actions'} className={'td-row-actions'}>
                        <i className={'expander fa fa-fw fa-' + (row.__collapsed ? 'plus' : 'minus') + '-square-o far fa-' + (row.__collapsed ? 'plus' : 'minus') + '-square'}
                           onClick={e => this.onExpanderClick(e)}
                        />

                        <i className={'drag-handler fa fas fa-fw fa-reorder fa-bars'} {...provided.dragHandleProps}/>
                    </td>
                );

                // Build TDs array
                Object.keys(row).forEach(k => {
                    if (this.props.fieldsTitles.hasOwnProperty(k)) {
                        const td = <td key={k}
                                       className={`td-field-${k}`}
                                       dangerouslySetInnerHTML={{__html: row[k]}}
                        />;

                        tds.splice(this.props.fields.indexOf(k) + 2, 0, td);
                    }
                });



                return <tr key={row.__id}
                           ref={provided.innerRef}
                           className={className + (snapshot.isDragging ? ' is-dragging' : '')}
                           {...provided.draggableProps}
                >
                    {tds}
                </tr>
            }}
        </Draggable>
    }
}

class TreeTable extends React.Component {
    static propTypes = {
        fetchRowsUrl: PropTypes.string.isRequired,
        fields: PropTypes.arrayOf(PropTypes.string).isRequired,
        fieldsTitles: PropTypes.object.isRequired,
        name: PropTypes.string.isRequired,
        updateRowsUrl: PropTypes.string.isRequired,
    };

    constructor(props) {
        super(props);

        this.state = {
            rows: [],
        };

        this.fetchRows = this.fetchRows.bind(this);
        this.getRowIndex = this.getRowIndex.bind(this);
        this.getRow = this.getRow.bind(this);
        this.getRowChildrenIds = this.getRowChildrenIds.bind(this);
        this.getRowChildren = this.getRowChildren.bind(this);
        this.isRowHasChild = this.isRowHasChild.bind(this);
        this.getRowDescendantsIds = this.getRowDescendantsIds.bind(this);
        this.getRowDescendants = this.getRowDescendants.bind(this);
        this.getRowAncestorsIds = this.getRowAncestorsIds.bind(this);
        this.getPreviousRow = this.getPreviousRow.bind(this);
        this.getNextRow = this.getNextRow.bind(this);
        this.isRowAncestorCollapsed = this.isRowAncestorCollapsed.bind(this);
        this.iterateRows = this.iterateRows.bind(this);
        this.hideRows = this.hideRows.bind(this);
        this.showRows = this.showRows.bind(this);
        this.collapseRow = this.collapseRow.bind(this);
        this.expandRow = this.expandRow.bind(this);
        this.sortRows = this.sortRows.bind(this);
        this.moveRow = this.moveRow.bind(this);
        this.combineRow = this.combineRow.bind(this);
        this.onCollapseRowClick = this.onCollapseRowClick.bind(this);
        this.onExpandRowClick = this.onExpandRowClick.bind(this);
        this.onDragEnd = this.onDragEnd.bind(this);
    }

    componentDidMount() {
        this.fetchRows();
    }

    fetchRows() {
        httpApi.get(this.props.fetchRowsUrl).then(data => {
            if (!data.hasOwnProperty('rows'))
                throw "Server response does not contain 'rows' key";

            this.setState({
                rows: this.sortRows(data.rows),
            });
        });
    }

    getRowIndex(rows, rowId) {
        for (let i = 0; i < rows.length; i++) {
            if (rows[i].__id === rowId)
                return i;
        }

        throw `Row with id==${rowId} is not found`;
    }

    getRow(rows, rowId) {
        return rows[this.getRowIndex(rows, rowId)];
    }

    getRowChildrenIds(rows, parentRowId) {
        const r = [];

        rows.forEach(row => row.__parent === parentRowId && r.push(row.__id));

        return r;
    }

    getRowChildren(rows, parentRowId) {
        return this.getRowChildrenIds(rows, parentRowId).map(rowId => this.getRow(rows, rowId));
    }

    isRowHasChild(rows, rowId) {
        for (const row of rows) {
            if (row.__parent === rowId)
                return true;
        }

        return false;
    }

    getRowDescendantsIds(rows, rowId, _acc = []) {
        for (const childId of this.getRowChildrenIds(rows, rowId)) {
            _acc.push(childId);
            if (this.isRowHasChild(rows, childId))
                this.getRowDescendantsIds(rows, childId, _acc);
        }

        return _acc;
    }

    getRowDescendants(rows, parentRowId) {
        return this.getRowDescendantsIds(rows, parentRowId).map(rowId => this.getRow(rows, rowId));
    }

    getRowAncestorsIds(rows, rowId, _acc = []) {
        const row = this.getRow(rows, rowId);
        if (row && row.__parent) {
            _acc.push(row.__parent);
            this.getRowAncestorsIds(rows, row.__parent, _acc);
        }

        return _acc;
    }

    getPreviousRow(rows, rowId) {
        const rowIndex = this.getRowIndex(rows, rowId);

        return rowIndex > 0 ? rows[rowIndex - 1] : null;
    }

    getNextRow(rows, rowId) {
        const rowIndex = this.getRowIndex(rows, rowId);

        return rowIndex < rows.length ? rows[rowIndex + 1] : null;
    }

    isRowAncestorCollapsed(rows, rowId) {
        for (const ancestorId of this.getRowAncestorsIds(rows, rowId)) {
            if (this.getRow(rows, ancestorId).__collapsed)
                return true;
        }

        return false;
    }

    iterateRows(rows, rowsIds, callback) {
        rows.slice().forEach(row => {
            if (rowsIds.indexOf(row.__id) >= 0)
                callback(row);
        });

        return rows;
    }

    hideRows(rows, rowsIds) {
        return this.iterateRows(rows, rowsIds, row => row.__hidden = true)
    }

    showRows(rows, rowsIds) {
        return this.iterateRows(rows, rowsIds, row => {
            // Show row only if its parent is not collapsed
            if (!this.isRowAncestorCollapsed(rows, row.__id))
                row.__hidden = false;
        })
    }

    collapseRow(rows, rowId) {
        // Collapse row
        rows = this.iterateRows(rows, [rowId], row => row.__collapsed = true);

        // Hide descendants of collapsed row
        rows = this.hideRows(rows, this.getRowDescendantsIds(rows, rowId));

        return rows;
    }

    expandRow(rows, rowId) {
        // Expand row
        rows = this.iterateRows(rows, [rowId], row => row.__collapsed = false);

        // Show children of expanded row
        rows = this.showRows(rows, this.getRowDescendantsIds(rows, rowId));

        return rows;
    }

    sortRows(rows, _parentId = null, _acc = []) {
        this.getRowChildren(rows, _parentId).forEach(row => {
            if (!row.hasOwnProperty('__id'))
                throw "Row doesn't have the '__id' property";
            if (!row.hasOwnProperty('__parent'))
                throw "Row doesn't have the '__parent' property";

            if (_parentId) {
                // Insert row after last appended child
                const appendedDescendantsCount = this.getRowDescendantsIds(_acc, row.__parent).length;
                const rowIndex = this.getRowIndex(_acc, _parentId) + 1 + appendedDescendantsCount;
                row.__depth = this.getRow(rows, row.__parent).__depth + 1;
                _acc.splice(rowIndex, 0, row);
            } else {
                row.__depth = 0;
                _acc.push(row);
            }

            if (this.isRowHasChild(rows, row.__id))
                this.sortRows(rows, row.__id, _acc);
        });

        return _acc;
    }

    moveRow(rows, srcIndex, dstIndex) {
        // Don't modify source array
        rows = rows.slice();

        // Remember source row before it will be removed by next splice() call
        const row = rows[srcIndex];

        // Delete
        rows.splice(srcIndex, 1);

        // Insert
        rows.splice(dstIndex, 0, row);

        // Change row's parent if necessary
        const prevRow = this.getPreviousRow(rows, row.__id);
        const nextRow = this.getNextRow(rows, row.__id);
        if (!(prevRow && nextRow))
            row.__parent = null;
        else if (prevRow.__parent === nextRow.__parent)
            row.__parent = prevRow.__parent;
        else if (nextRow.__parent === prevRow.__id)
            row.__parent = prevRow.__id;

        return this.sortRows(rows);
    }

    combineRow(rows, srcId, dstId) {
        // Don't modify source array
        rows = rows.slice();

        this.getRow(rows, srcId).__parent = this.getRow(rows, dstId).__id;

        return this.expandRow(this.sortRows(rows), dstId);
    }

    onCollapseRowClick(rowId) {
        this.setState({
            rows: this.collapseRow(this.state.rows, rowId),
        });
    }

    onExpandRowClick(rowId) {
        this.setState({
            rows: this.expandRow(this.state.rows, rowId),
        });
    }

    onDragEnd(result) {
        let rows;

        if (result.combine)
            rows = this.combineRow(this.state.rows, result.draggableId, result.combine.draggableId);
        else
            rows = this.moveRow(this.state.rows, result.source.index, result.destination.index);

        // Update component's state to immediately reflect changes
        this.setState({rows: rows});

        // Update data on the server, then update component's state
        const putRowsData = rows.map((row, index) => ({
            __id: row.__id,
            __parent: row.__parent,
            order: (index * 10) + 10,
        }));
        httpApi.put(this.props.updateRowsUrl, {rows: JSON.stringify(putRowsData)})
            .catch(() => window.location.reload());
    };

    render() {
        return <DragDropContext onDragEnd={this.onDragEnd}>
            <Table className={'table-striped table-bordered table-hover'}>
                <thead>
                <tr>
                    <th className={'th-row-actions'}>&nbsp;</th>
                    {this.props.fields.map(fName => (
                        <th key={fName} className={`th-field-${fName}`}>{this.props.fieldsTitles[fName]}</th>
                    ))}
                </tr>
                </thead>

                <Droppable droppableId={`tree-table-${this.props.name}`} type={`tree-table-${this.props.name}`}
                           isCombineEnabled>
                    {provided => (
                        <tbody ref={provided.innerRef}>
                        {this.state.rows.map(row => {
                            const rowIndex = this.getRowIndex(this.state.rows, row.__id);

                            return <Row fields={this.props.fields}
                                        fieldsTitles={this.props.fieldsTitles}
                                        hasChildren={this.isRowHasChild(this.state.rows, row.__id)}
                                        index={rowIndex}
                                        key={rowIndex}
                                        onCollapseClick={this.onCollapseRowClick}
                                        onExpandClick={this.onExpandRowClick}
                                        rowData={row}
                            />
                        })}
                        </tbody>
                    )}
                </Droppable>
            </Table>
        </DragDropContext>
    }
}

setupWidget('plugins.widget._misc.TreeTable', widget => {
    const fields = [];
    const fieldsTitles = {};
    widget.data('fields').split(',').forEach(fieldData => {
        const fieldDataSplit = fieldData.split(':');
        fields.push(fieldDataSplit[0]);
        fieldsTitles[fieldDataSplit[0]] = fieldDataSplit[1];
    });

    ReactDOM.render(<TreeTable fetchRowsUrl={widget.data('rowsUrl')}
                               fields={fields}
                               fieldsTitles={fieldsTitles}
                               name={widget.uid}
                               updateRowsUrl={widget.data('updateRowsUrl')}

    />, widget.find('.widget-component')[0]);
});
