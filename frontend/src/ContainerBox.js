import { memo, useCallback, useMemo, useState } from 'react'
import { useDrag, useDrop } from 'react-dnd'
import { Colors } from './Colors.js'

const style = {
    border: '1px solid #ccc',
    padding: '1rem',
    margin: '1rem',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#f9f9f9',
    transition: 'background-color 0.3s, box-shadow 0.3s',
}

const buttonStyle = {
    margin: '0.5rem',
    padding: '0.5rem 1rem',
    border: '1px solid #ccc',
    borderRadius: '4px',
    backgroundColor: '#fff',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    cursor: 'pointer',
    transition: 'background-color 0.3s, box-shadow 0.3s',
}

const FieldType = {
    NUMBER: 'number',
    BOOL: 'bool',
    STRING: 'string',
    CONTAINER: 'container',
    TABLE: 'table',
    GENERATOR: 'generator',
    CHOICE: 'choice',
    SINGLE: 'single',
}

const BOX_COLORS = [Colors.WHITE, Colors.GRAY, Colors.RED]

const ROOT_NAME = '__NAME__FOR__DATA__PLEASE__DO__NOT__USE__THIS__NAME__'

export function createFields(embedifiedTemplate, parent_path, depth = 0) {
    if (parent_path === null) {
        parent_path = ROOT_NAME
        return [ContainerBox({
            color: BOX_COLORS[depth % 2],
            path: parent_path,
            children: createFields(embedifiedTemplate, '', depth + 1)
        })]
    }
    let children = []
    for (let field_name in embedifiedTemplate) {
        let s_or_t = embedifiedTemplate[field_name]
        let new_path = parent_path + '.' + field_name
        if (s_or_t instanceof Object) {
            children.push(ContainerBox({
                color: BOX_COLORS[depth % 2],
                path: new_path,
                children: createFields(embedifiedTemplate[field_name], new_path, depth + 1)
            }))
        } else {
        }
    }
    return children
}

export const ContainerBox = function ContainerBox({ color, path, children }) {
    let name = path.split('.').pop()

    const [{ isDragging }, drag] = useDrag(
        () => ({
            type: FieldType.CONTAINER,
            item: { color, type: FieldType.CONTAINER },
            canDrag: name !== ROOT_NAME,
            collect: (monitor) => ({
                isDragging: !!monitor.isDragging(),
            }),
            end: (dropResult, monitor) => {
                if (monitor.didDrop()) {
                }
            }
        }),
        [color],
    )

    const [{ isOver, isOverCurrent, canDrop }, drop] = useDrop({
        accept: [FieldType.CONTAINER, FieldType.NUMBER, FieldType.BOOL, FieldType.STRING, FieldType.TABLE, FieldType.GENERATOR, FieldType.CHOICE, FieldType.SINGLE],
        collect: (monitor) => ({
            isOver: !!monitor.isOver(),
            isOverCurrent: !!monitor.isOver({ shallow: true }),
            canDrop: !!monitor.canDrop()
        }),
        drop: (item, monitor) => {
            console.log(children)
        },
    })
    if (canDrop && isOverCurrent) {
        color = Colors.YELLOW
    }

    const containerStyle = {
        ...style,
        background: color,
        opacity: isDragging ? 0.2 : 1,
        cursor: 'move',
        overflowY: 'auto',
        ...(path === ROOT_NAME ? { height: '95vh' } : {}),
    }

    return (
        <div ref={(node) => drag(drop(node))} style={containerStyle} role="ContainerBox" data-color={color}>
            {path === ROOT_NAME && (
                <div className="container-info"
                     style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>Template Builder</span>
                </div>
            )}
            {path !== ROOT_NAME && (
                <div>
                    <div className="container-info"
                         style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <span>Container</span>
                        <button className="delete-button"
                                style={{ ...buttonStyle, background: 'red', color: 'white' }}>X
                        </button>
                    </div>
                    <div className="container-info"
                         style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <span type="text">{name}</span>
                    </div>
                </div>)}
            {children}
        </div>
    )
}

export const BasicBox = function BasicBox({ color, path, field_type }) {
    let name = path.split('.').pop()

    const [{ isDragging }, drag] = useDrag(
        () => ({
            type: FieldType.CONTAINER,
            item: { color, type: FieldType.CONTAINER },
            canDrag: true,
            collect: (monitor) => ({
                isDragging: !!monitor.isDragging(),
            }),
            end: (dropResult, monitor) => {
                if (monitor.didDrop()) {
                }
            }
        }),
        [color],
    )

    const containerStyle = {
        ...style,
        background: Colors.BLUE,
        opacity: isDragging ? 0.2 : 1,
        cursor: 'move',
    }

    return (
        <div ref={(node) => drag} style={containerStyle} role="ContainerBox" data-color={color}>
            <div className="field-info"
                 style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span>{field_type}</span>
                <button className="delete-button" style={{ ...buttonStyle, background: 'red', color: 'white' }}>X
                </button>
            </div>
            <div className="field-info"
                 style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span type="text">{name}</span>
            </div>
        </div>
    )
}