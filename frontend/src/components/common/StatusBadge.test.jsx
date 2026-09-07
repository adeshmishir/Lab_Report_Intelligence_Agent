import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { StatusBadge } from './StatusBadge'

describe('StatusBadge', () => {
  it('translates quality enums into user-facing labels', () => {
    render(<StatusBadge status="conflicting_values" />)
    expect(screen.getByText('Conflicting result')).toBeInTheDocument()
  })
})