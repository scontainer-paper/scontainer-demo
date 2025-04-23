import {createRoot} from 'react-dom/client'
import {Container} from './Container.js'
import {DndProvider} from 'react-dnd'
import {HTML5Backend} from 'react-dnd-html5-backend'
import {StrictMode, useState} from 'react'
import {NewFieldBox} from "./ContainerBox";

function App() {
    let [isOpen, setIsOpen] = useState(false)
    return (
        <div className="App" style={{display: 'flex'}}>
            <DndProvider backend={HTML5Backend}>
                <div style={{
                    width: '200px',
                    border: '2px solid #ccc',
                    borderRadius: '8px',
                    padding: '1rem',
                    display: 'flex',
                    flexDirection: 'column',
                    margin: '1rem',
                    backgroundColor: '#f9f9f9',
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                    transition: 'background-color 0.3s, box-shadow 0.3s'
                }}>
                    <NewFieldBox label={"String"}/>
                    <NewFieldBox label={"Number"}/>
                    <NewFieldBox label={"Bool"}/>
                    <NewFieldBox label={"Container"}/>
                </div>
                <div style={{flex: 1, padding: '1rem', flexDirection: 'column', margin: '1rem'}}>
                    <Container/>
                </div>
            </DndProvider>
        </div>
    )
}

const rootElement = document.getElementById('root')
const root = createRoot(rootElement)
const RootComponent = () => (
    <StrictMode>
        <App/>
    </StrictMode>
)
root.render(<RootComponent/>)
