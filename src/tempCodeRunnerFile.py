    board.set_hover(motion_row, motion_col)
                    self.is_update_needed = True

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        self.is_update_needed = True