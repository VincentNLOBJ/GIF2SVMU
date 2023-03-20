*******************************************************
*                      FUNCTION                       *
*******************************************************
; LAUNCH_SVMU_ANIMATION()

sts.l     PR,@-r15=>local_4
mov.l     ->DEFAULT_FRAME_DELAY,r0    
mov.l     ->CURRENT_TIMER,r2       
mov.l     ->ANIM_SCRIPTS,r4=>                                      
mov.l     ->TIMINGS,r3         
mov.l     ->VMU_GFX_POINTERS,r5  
mov.w     DEFAULT_FRAME_DELAY,r1             
mov.w     r1,@r0=>DEFAULT_FRAME_DELAY 
mov.l     ->SVMU_ANIMATION,r0      
jsr       @r0=>SVMU_ANIMATION      
_nop
lds.l     @r15+,PR
rts
_nop


;data

addr      PTR_ANIM_SCRIPTS 
addr      PTR_TIMINGS
addr      PTR_CURRENT_TIMER
addr      PTR_SVMU_ANIMATION
addr      PTR_VMU_GFX_POINTERS       
addr      DEFAULT_FRAME_DELAY         = 0030h
