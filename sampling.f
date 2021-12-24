      PROGRAM SAMPLING
      IMPLICIT NONE

      CHARACTER(LEN=120) LINE 
      CHARACTER(LEN=120) LINES
      DIMENSION LINES(500) 
      CHARACTER(LEN=48) INFILE, ARG

      CHARACTER(LEN=6) PERS_START
      CHARACTER(LEN=6) PERS_END
      CHARACTER(LEN=6) PERS_POND
      CHARACTER(LEN=6) STR

      DOUBLE PRECISION W, PROP
      INTEGER I, NL, N

      PERS_START="<perso"
      PERS_END  ="</pers"
      PERS_POND ="<!--"

      CALL GETARG(1, ARG)
      READ(ARG,'(F10.5)') PROP
      CALL GETARG(2, INFILE)

C     OPEN(10,FILE=INFILE)
C     READ(10,'(F9.3)') PROP
C     CLOSE(10)

      OPEN(1, FILE=INFILE) 

      READ(1, '(A120)') LINE 
      PRINT '(A38)', ADJUSTL(LINE)
      READ(1, '(A120)') LINE 
      PRINT '(A120)', ADJUSTL(LINE)
      PRINT*
      PRINT*, "<population>"
      PRINT*
      READ(1,*)
      READ(1,*)
      READ(1,*)
      READ(1, '(A120)') LINE 
      PRINT '(A120)', LINE
      READ(1, '(A120)') LINE 
      PRINT '(A120)', LINE
      READ(1, '(A120)') LINE 
      PRINT '(A120)', LINE
      PRINT* 

  10  CONTINUE 

      READ(1, '(A120)',END=200) LINE 

      IF (LINE(3:8).EQ.PERS_START) THEN
        NL = 1
        LINES(NL) = LINE
        GOTO 10
      ELSEIF(LINE(3:8).EQ.PERS_END) THEN
        NL = NL + 1
        LINES(NL) = LINE
        CALL PRTPERSON(N,NL,LINES)
        GOTO 10
      ELSEIF(LINE(3:6).EQ.PERS_POND) THEN
        READ(LINE(8:14),'(F7.3)') W
        N = NINT(2.D0*RAND()*W*PROP)
      ENDIF 

      NL = NL + 1
      LINES(NL) = LINE 

      GOTO 10 

 200  CONTINUE

      PRINT*, "</population>"
      CLOSE(1)

      END


      SUBROUTINE PRTPERSON(N,NL,LINES) 
      IMPLICIT NONE

      CHARACTER(LEN=120) LINES
      DIMENSION LINES(500) 
      CHARACTER(LEN=120) LINE, LL
      CHARACTER(LEN=120) STR
      CHARACTER(LEN=4) ID
      DOUBLE PRECISION X, Y, XHOME, YHOME, XWORK, YWORK, RX, RY
      INTEGER N, NL, I, J, IHOME, IWORK, IXY
      INTEGER I1,I2

      RX = 1000.D0
      RY = 1000.D0 

      LINE=LINES(1)
      I1 = SCAN(LINE,'"')
      LINE = LINE(I1+1:120)
      I2 = SCAN(LINE,'"')
      LL = LINE(1:I2-1) 

      DO 10, I = 1, N
      WRITE(ID,'(I4.4)') I
      STR = '  <person id="'//TRIM(LL)//"_"//TRIM(ID)//'">'
      LINES(1) = STR
      IHOME = 0
      IWORK = 0
      DO 10, J = 1, NL
      LINE = LINES(J)
      CALL TESTXY(LINE,IXY)
      IF (IXY.EQ.1.AND.IHOME.EQ.0) THEN
        CALL COLLECTXY(LINE,X,Y)
        CALL NEWLINE(LINE, X, Y, RX, RY, 1)
        XHOME = X
        YHOME = Y
        IHOME = 1
      ELSEIF(IXY.EQ.1.AND.IHOME.EQ.1) THEN
        CALL NEWLINE(LINE, XHOME, YHOME, RX, RY, 0)
      ELSEIF (IXY.EQ.2.AND.IWORK.EQ.0) THEN
        CALL COLLECTXY(LINE,X,Y)
        CALL NEWLINE(LINE, X, Y, RX, RY, 1)
        XWORK = X
        YWORK = Y
        IWORK = 1
      ELSEIF(IXY.EQ.2.AND.IWORK.EQ.1) THEN
        CALL NEWLINE(LINE, XWORK, YWORK, RX, RY, 0)
      ELSEIF(IXY.GT.2) THEN
        CALL COLLECTXY(LINE,X,Y)
        CALL NEWLINE(LINE, X, Y, RX, RY, 1)
      ENDIF
      IF(J.NE.2) PRINT *, LINE
  10  CONTINUE 

      RETURN
      END 


      SUBROUTINE COLLECTXY(LINE, X, Y)
      IMPLICIT NONE

      CHARACTER(LEN=120) LINE
      DOUBLE PRECISION X, Y
      INTEGER I1, I2

      I1=INDEX(LINE,"x=")
      I2=INDEX(LINE,"y=") 
      READ(LINE(I1+3:I2-3),*) X
      I1 = I2
      I2=INDEX(LINE,"start_") 
      READ(LINE(I1+3:I2-3),*) Y 


      RETURN
      END

      SUBROUTINE TESTXY (LINE,IXY)
      IMPLICIT NONE

      CHARACTER(LEN=120) LINE
      INTEGER IXY, I

      IXY = 0

      IF(INDEX(LINE, "home").GT.1) IXY = 1
      IF(INDEX(LINE, "work").GT.1) IXY = 2
      IF(INDEX(LINE, "leisure").GT.1) IXY = 3
      IF(INDEX(LINE, "shop").GT.1) IXY = 3
      IF(INDEX(LINE, "education").GT.1) IXY = 3 


      RETURN
      END

      SUBROUTINE NEWLINE(LINE, X, Y, RX, RY, ID)
      IMPLICIT NONE
      CHARACTER(LEN=120) LINE
      CHARACTER(LEN=13) XCHAR
      CHARACTER(LEN=13) YCHAR
      DOUBLE PRECISION X, Y, RX, RY
      INTEGER I1, I2, I3, ID
      INTEGER IX1,IX2,IY1,IY2 

      I1 = INDEX(LINE, "x=")
      I2 = INDEX(LINE, "y=")
      I3 = INDEX(LINE, "start_")

      IF(ID.EQ.0) GOTO 10

      READ(LINE(I1+3:I2-3),*) X
      READ(LINE(I2+3:I3-3),*) Y 
      CALL COLLECTXY(LINE, X, Y)

      X = X + ( RAND() - 0.5D0 ) * RX
      Y = Y + ( RAND() - 0.5D0 ) * RY

 10   CONTINUE

      IF(I2-I1.EQ.19) THEN
         WRITE(XCHAR, '(F13.5)') X
      ELSE
         WRITE(XCHAR, '(F13.5)') X 
      ENDIF 
      WRITE(YCHAR, '(F13.5)') Y

      LINE=LINE(1:I1+2)//XCHAR//LINE(I2-2:I2+2)//YCHAR//LINE(I3-2:120)

      RETURN
      END



