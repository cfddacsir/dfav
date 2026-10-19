Function getlib( ){
  $LIB = @{} ;
  $LIBPATH=(
    "G:\My Drive\mylab\", 
    "G:\My Drive\mylab\lib\"  ,"G:\My Drive\mylab\star\" 
  );
  $pystar=$LIBPATH[2]   + "pystar.py"
  $postjava=$LIBPATH[2] + "post_batch.java" ;
  $LIB = @{};
  $LIB.add( 'lab',      $LIBPATH[0]    );
  $LIB.add( 'lib',      $LIBPATH[1]    );
  $LIB.add( 'star',     $LIBPATH[2]    );
  $LIB.add( 'pystar',   $pystar        );
  $LIB.add( 'postjava', $postjava      );
  return $LIB ;
  ##< 2024-02-09-17z18 >##

}
    $LIB=(getlib) 
    $postjava=$LIB['postjava']
    $pystar=$LIB['pystar']

    " {0:s} = {1:s} " -f "pystar"   , $pystar  ;
    " {0:s} = {1:s} " -f "postjava" , $postjava  ;
