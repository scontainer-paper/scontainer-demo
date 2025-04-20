import { memo } from 'react'
import { Colors } from './Colors.js'
import { ContainerBox, createFields } from './ContainerBox.js'
import { StatefulTargetBox as TargetBox } from './TargetBox.js'
export const Container = function Container() {
  // let boxes = createFields({ a: { b: { c: 'number', d: 'number' }, e: { f: 'number' } } }, null)
  // create a test dict with 100 fields;
    let test_dict = {}
    for (let i = 0; i < 100; i++) {
        test_dict[i] = { a: 'number', b: 'number' }
    }
    let test_boxes = createFields(test_dict, null)



  return (
    <div style={{ overflow: 'hidden', clear: 'both', margin: '-.5rem', height: '100vh' }}>
      { test_boxes }
    </div>
  )
}
