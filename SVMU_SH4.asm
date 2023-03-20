     *******************************************************
     *                      FUNCTION                       *
     *******************************************************
     ;SVMU_ANIMATION()

          sts.l     PR,@-r15=>local_4

     ;read_timer_PTR_from_r2
          mov.l     @r2,r2
          bra       current_animation_loop
          _mov      #0x0,r0

     ;next_animation                         
          add       #0x2,r3
          add       #0x1,r0

     ;current_animation_loop                 
          mov.w     @r3,r1
          extu.w    r1,r1
          cmp/gt    r1,r2
          bt        next_animation

     ;r0=animation num
     ;r1=current_timing
     ;r2=scene_timer

          mov.l     ->ANIMATION_NUM,r9          
          mov.l     ->CURRENT_FRAME_TIMER,r7=>  
          mov.l     ->CURRENT_ANIM_FRAME,r8     
          mov       #0x0,r3
		  
     ;if_current_scene_timer_is_0
          cmp/eq    r2,r3
          bt        RESET_frame_timer&current
		  
     ;if_animation_timer=cur_timing
          cmp/eq    r1,r2
          bf        write_animation_num
		  
     ;next_animation
          add       #0x1,r0
		  
     ;RESET_frame_timer&current_frame        
          mov.l     r3,@r7=>CURRENT_FRAME_TIMER
          mov.l     r3,@r8=>CURRENT_ANIM_FRAME
		  
     ;write_animation_num                   
          mov.l     r0,@r9=>ANIMATION_NUM
          shll2     r0
		  
     ;animation_pointer_in_r4
          add       r0,r4
		  
     ;read_default_delay
          mov.w     DEFAULT_FRAME_DELAY,r1      = 0030h
          mov.l     @r7=>CURRENT_FRAME_TIMER,r2
          mov.l     @r8=>CURRENT_ANIM_FRAME,r3
		  
     ;if_frame_timer=delay
          cmp/eq    r2,r1
          bf        read_script_value_in_r0
		  
     ;next_frame
          mov       #0x0,r1
          mov.l     r1,@r7=>CURRENT_FRAME_TIMER
          add       #0x1,r3
          mov.l     r3,@r8=>CURRENT_ANIM_FRAME
		  
     ;read_script_value_in_r0                 
          mov.l     @r4,r0
          add       r3,r0
          mov.b     @r0,r0
          cmp/eq    #-0x1,r0
		  
     ;if_control_code=0xFF_loop
          bf        if_control_code=0xFE_no_lo
          mov       #0x0,r1
          mov.l     r1,@r7=>CURRENT_FRAME_TIMER
          mov.l     r1,@r8=>CURRENT_ANIM_FRAME
          bra       return
          _nop
		  
     ;if_control_code=0xFE_no_loop          
          cmp/eq    #-0x2,r0
          bf        *VMU_control*,script_value
          mov       #0x1,r1
          mov.l     r1,@r7=>CURRENT_FRAME_TIMER
          bra       return
          _nop
		  
     ;*VMU_control*,script_value*4           
          shll2     r0
		  
     ;add_value_to_first_gfx_pointer
          add       r0,r5
		  
     ;read_target_gfx_pointer
          mov.l     @r5,r5
          mov.l     @r7=>CURRENT_FRAME_TIMER,r0
		  
     ;if_current_frame_timer=0_(display_GFX)
          cmp/eq    #0x0,r0
          bf        increase_timer
		  
     ;display_VMU_GFX
          mov       #0x1,r4
          mov       #0x0,r3
          mov.l     ->_pdVmsLcdWrite1,r0        
          jsr       @r0=>_pdVmsLcdWrite1        
          _nop
		  
     ;increase_timer                          
          mov.l     ->CURRENT_FRAME_TIMER,r1    
          mov.l     @r1=>CURRENT_FRAME_TIMER,r0
          add       #0x1,r0
          mov.l     r0,@r1=>CURRENT_FRAME_TIMER
		  
     ;return                                 
          lds.l     @r15+,PR
          rts
          _nop


    ; data
    PTR_ANIMATION_NUM
    PTR_CURRENT_ANIM_FRAME 
    PTR__pdVmsLcdWrite1
    PTR_CURRENT_FRAME_TIMER
    DEFAULT_FRAME_DELAY    0030
