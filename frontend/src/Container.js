import {createFields, renderTemplate} from './ContainerBox.js'

export const Container = function Container() {
    return (
        <div style={{overflow: 'hidden', clear: 'both', margin: '-.5rem', height: '100vh'}}>
            {renderTemplate()}
        </div>
    );
};