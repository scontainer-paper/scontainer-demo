import {useDrag, useDrop} from 'react-dnd'
import {Colors} from './Colors.js'


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
    NUMBER: 'Number',
    BOOL: 'Bool',
    STRING: 'String',
    CONTAINER: 'Container',
    TABLE: 'Table',
    GENERATOR: 'Generator',
    BASIC: 'Basic'
}

const BOX_COLORS = [Colors.WHITE, Colors.GRAY, Colors.RED]

const ROOT_NAME = '__NAME__FOR__DATA__PLEASE__DO__NOT__USE__THIS__NAME__'

var template = window.localStorage.getItem('scontainer_template') === null ? require('./var.js') : JSON.parse(window.localStorage.getItem('scontainer_template'))
var paths = {}

export function renderTemplate() {
    return createFields(template, null)
}


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
        let new_path = parent_path === '' ? field_name : parent_path + '.' + field_name
        if (s_or_t instanceof Object) {
            children.push(ContainerBox({
                color: BOX_COLORS[depth % 2],
                path: new_path,
                children: createFields(s_or_t, new_path, depth + 1)
            }))
        } else {
            paths[new_path] = s_or_t
            children.push(BasicBox({
                color: BOX_COLORS[depth % 2],
                path: new_path,
                field_type: s_or_t
            }))
        }
    }
    return children
}


const OpType = {
    INSERT: 'INSERT',
    DELETE: 'DELETE',
    MOVE: 'MOVE',
}

function request(op, src, dst, type = null) {
    var newpaths = []
    for (const [key, value] of Object.entries(paths)) {
        newpaths.push([key, value])
    }

    var body = {op_type: op, template: newpaths}
    if (op === OpType.INSERT) {
        body['dst'] = dst
        body['src'] = src
        body['add_type'] = type
    } else if (op === OpType.DELETE) {
        body['src'] = src
    } else if (op === OpType.MOVE) {
        if (dst === ROOT_NAME) {
            dst = null
        }
        body['src'] = src
        body['dst'] = dst
    }
    const headers = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    }
    fetch('/template/', headers)
        .then(response => response.json())
        .then(data => {
            window.localStorage.setItem('scontainer_template', JSON.stringify(data.nested_template))
            var before = ''
            for (const [key, value] of Object.entries(paths)) {
                before += '<' + key + '>: ' + value + '\n'
            }
            console.log(before)
            showModal('Before: ' + '\n' + before + '\n' + 'After: ' + '\n' + data.template).then(
                () => {
                    window.location.reload()
                }
            )
        });
}

export const ContainerBox = function ContainerBox({color, path, children}) {
    let name = path.split('.').pop()

    const [{isDragging}, drag] = useDrag(
        () => ({
            type: FieldType.CONTAINER,
            item: {isNew: false, src: path, type: FieldType.CONTAINER},
            canDrag: name !== ROOT_NAME,
            collect: (monitor) => ({
                isDragging: !!monitor.isDragging(),
            }),
            end: (dropResult, monitor) => {
                if (monitor.didDrop()) {

                }
            }
        }),
    )

    const [{isOver, isOverCurrent, canDrop}, drop] = useDrop({
        accept: [FieldType.CONTAINER, FieldType.BASIC],
        collect: (monitor) => ({
            isOver: !!monitor.isOver(),
            isOverCurrent: !!monitor.isOver({shallow: true}),
            canDrop: !!monitor.canDrop()
        }),
        drop(item, monitor) {
            if (monitor.isOver({shallow: true}) && !monitor.didDrop()) {
                if (!item.isNew) {
                    request(OpType.MOVE, item.src, path)
                } else {
                    const newName = prompt("Enter a name for the new field:");
                    if (newName) {
                        request(OpType.INSERT, newName, path === ROOT_NAME ? null : path, item.label)
                    }
                }
            }
        },
        canDrop(item, monitor) {
            if (item.isNew) {
                return true
            }
            if (item.src === path) {
                return false
            }
            var p = item.src.split('.')
            p.pop()
            if (p.length === 0) {
                p = [ROOT_NAME]
            }
            return path !== p.join('.')
        }
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
        ...(path === ROOT_NAME ? {height: '95vh'} : {}),
    }

    return (
        <div ref={(node) => drag(drop(node))} style={containerStyle} role="ContainerBox" data-color={color}>
            {path === ROOT_NAME && (
                <div className="container-info"
                     style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                    <span style={{fontWeight: 'bold', fontSize: '1.2rem'}}>Template Builder</span>
                </div>
            )}
            {path !== ROOT_NAME && (
                <div>
                    <div className="container-info"
                         style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                        <span>Container</span>
                        <button className="delete-button" style={{...buttonStyle, background: 'red', color: 'white'}}
                                onClick={() => request(OpType.DELETE, path, null)}>X
                        </button>
                    </div>
                    <div className="container-info"
                         style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                        <span type="text">{name}</span>
                    </div>
                </div>)}
            {children}
        </div>
    )
}

export const BasicBox = function BasicBox({color, path, field_type}) {
    let name = path.split('.').pop()

    const [{isDragging}, drag] = useDrag(
        () => ({
            type: FieldType.CONTAINER,
            item: {isNew: false, src: path, type: FieldType.BASIC},
            canDrag: name !== ROOT_NAME,
            collect: (monitor) => ({
                isDragging: !!monitor.isDragging(),
            }),
            end: (dropResult, monitor) => {
                if (monitor.didDrop()) {

                }
            }
        }),
        [template],
    )

    const containerStyle = {
        ...style,
        background: Colors.BLUE,
        opacity: isDragging ? 0.2 : 1,
        cursor: 'move',
    }

    return (
        <div ref={drag} style={containerStyle} role="BasicBox" data-color={color}>
            <div className="field-info"
                 style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                <span>{field_type}</span>
                <button className="delete-button" style={{...buttonStyle, background: 'red', color: 'white'}}
                        onClick={() => request(OpType.DELETE, path, null)}>X
                </button>
            </div>
            <div className="field-info"
                 style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                <span type="text">{name}</span>
            </div>
        </div>
    )
}


export function NewFieldBox({label}) {

    const type_ = label === 'Container' ? FieldType.CONTAINER : FieldType.BASIC
    const [{isDragging}, drag] = useDrag(
        () => ({
            type: type_,
            item: {isNew: true, type: type_, label: label},
            collect: (monitor) => ({
                isDragging: !!monitor.isDragging(),
            }),
            end: (dropResult, monitor) => {
                if (monitor.didDrop()) {

                }
            }
        }),
        [template],
    )


    return (
        <button ref={drag} style={{
            margin: '0.5rem',
            padding: '0.5rem 1rem',
            border: '1px solid #ccc',
            borderRadius: '4px',
            backgroundColor: '#fff',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
            cursor: 'pointer',
            transition: 'background-color 0.3s, box-shadow 0.3s'
        }}>
            {label}
        </button>
    )
}

function closeModal() {
    document.body.removeChild(document.querySelector('div'));
}

function showModal(message) {
    message = message.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    message = message.replace(/\n/g, '<br>');
    return new Promise((resolve) => {
        // Create an overlay to block all interactions
        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100vw';
        overlay.style.height = '100vh';
        overlay.style.background = 'rgba(0, 0, 0, 0.5)';
        overlay.style.zIndex = '999'; // Ensure it is above all other elements
        document.body.appendChild(overlay);

        // Create a modal
        const modal = document.createElement('div');
        modal.style.position = 'fixed';
        modal.style.top = '50%';
        modal.style.left = '50%';
        modal.style.transform = 'translate(-50%, -50%)';
        modal.style.background = '#fff';
        modal.style.padding = '20px';
        modal.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';
        modal.style.zIndex = '1000'; // Ensure it is above the overlay
        modal.innerHTML = message + '<br><button id="closeModalButton">Close</button>';
        document.body.appendChild(modal);

        document.getElementById('closeModalButton').onclick = () => {
            document.body.removeChild(modal);
            document.body.removeChild(overlay); // Remove the overlay
            resolve(); // Resolve the promise when the modal is closed
        };
    });
}
