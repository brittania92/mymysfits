import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import TheGrid from '../TheGrid.vue'

describe('TheGrid.vue Test', () => {
  it('Has a good/evil menu', () => {
      
    // render the component
    const wrapper = shallowMount(TheGrid, { })

    // check that the title is rendered
    const menuDiv = wrapper.findAll('#filterMenu').at(0)
    expect(menuDiv.findAll('button').at(0).text()).toMatch('Good')
    expect(menuDiv.findAll('button').at(1).text()).toMatch('Neutral')
    expect(menuDiv.findAll('button').at(2).text()).toMatch('Evil')
  }),
  it('Has a law/chaos menu', () => {
      
    // render the component
    const wrapper = shallowMount(TheGrid, { })

    // check that the title is rendered
    const menuDiv = wrapper.findAll('#filterMenu').at(1)
    expect(menuDiv.findAll('button').at(0).text()).toMatch('Lawful')
    expect(menuDiv.findAll('button').at(1).text()).toMatch('Neutral')
    expect(menuDiv.findAll('button').at(2).text()).toMatch('Chaotic')
  })
})