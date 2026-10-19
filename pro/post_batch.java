/* /////////////////////////////////////////////////////////////////////////////
 * FILE:    post_batch.java
 * TYPE:    starccm_java_macro   //{ Simcenter STAR-CCM+ macro 16.06.008 }//
 * PERS:    'Daniel.Collins@wisk.aero' 
 * LAST:    '2024-04-13-14:01Z': +save_plottab ( basename )... 
 * PURP:    'generate Reports, Plots and Scenes in STARCCM+ model based on
               keys listed in {TABPATH\reports.csv, TABPATH\scenes.csv} 
               where TABPATH is pathway specified in main class.
//////////////////////////////////////////////////////////////////////////////*/
package macro;

import star.common.*;
import star.base.neo.*;
import star.base.query.*;
import star.base.report.*;
import star.vis.*;
import star.common.Tag; 
import star.common.UserTag ; 
import star.flow.*;
import star.circuit.*;
import star.energy.* ; 

import java.io.*;
import java.io.File;
import java.io.Reader;
import java.io.FileReader;
import java.io.BufferedReader;
import java.util.*;
import java.util.stream.*;
import java.util.stream.Stream;
import java.util.stream.Collectors;
import java.lang.String.*;
import java.lang.Object;
import java.io.Reader; 
//import java.Parser ;


////////////////////////////////////////////////////////////////////////////////

public class post_batch extends StarMacro {

public void execute( /*String TABPATH*/ ) {
    ////  Specific Values ///-------------------------------------
    String TABPATH = "";String TABPREF ="";String TABSUFF ="";
    
    TABPATH = "G:\\My Drive\\mylab\\star\\cobalt\\";
    TABPATH = "G:\\My Drive\\mylab\\star\\hg\\";
    TABPREF = "";
    TABSUFF = "-hg";
    
    boolean[] EX = new boolean[30] ; 
    EX[0] = false ; 
    EX[1] = true  ; // read-table
    EX[2] = false ; 
    EX[2] = false ; 
    //boolean[] QE = {false , true };
    
    boolean[] CX = new boolean[30] ; 
    CX[0] = false ; // run-all
    CX[1] = true  ; // run-reports 
    CX[2] = true  ; // run-scenes  


    //// Persistent ... ///-------------------------------------
    Simulation thissim = getActiveSimulation();
    String CWDIR = thissim.getSessionDir() + "\\" ;
    String sep = System.getProperty("file.separator"); //get the right separator for your operative system

    String bbe = "=".repeat(72) ;
    String bba = "-".repeat(72) ;

    thissim.println( bbe ) ;
    System.out.println( bbe ) ;

        //String REPDIR ; REPDIR = CWDIR + "rep";
        //File  MKDIR = new File(REPDIR) ;MKDIR.mkdir();
    (new File(CWDIR+sep + "post"   )).mkdir();          
    //(new File(CWDIR+sep + "rep"    )).mkdir();
    //(new File(CWDIR+sep + "ssa"    )).mkdir();
    //(new File(CWDIR+sep + "plots"  )).mkdir();
    //// Main Execution Loop ///-------------------------------------
    
    List<String> exo_post = Arrays.asList( 
        "reports" ,
        "scenes" 
    );
    
    for ( String exo  : exo_post ) {
        String csv_name = resolvePath(TABPATH + TABPREF + exo + TABSUFF + ".csv" ); 
        Dictionary map = readtable (csv_name, EX ) ;
        runhash( map, exo, EX, CX ) ;
    }
    //  
        thissim.println(String.format(
            "Congratulations, you have completed this macro. " )
        );
        System.out.println(String.format(
            "Congratulations, you have completed this macro. " )
        );
        echo_br(); 
}/// public void execute()

////////////////////////////////////////////////////////////////////////////
public void runhash ( Dictionary<String,String> map, String whattodo, boolean[] EX, boolean[] CX ){	
    // CASE OF SCENES, PLOT, HISTOGRAMS
    Simulation thissim = getActiveSimulation();
    String CWDIR = thissim.getSessionDir() + "\\" ;
    String sep = System.getProperty("file.separator"); //get the right separator for your operative system
       
    //// Read Hashtable 

        Enumeration<String> keys = map.keys();
        System.out.println( keys );
        while (keys.hasMoreElements()) {
            String key = keys.nextElement();
            String ktype = map.get(key); 
            
            /// char a = "#".charAt(0) ;
            // Java String startsWith() Method
            // https://www.w3schools.com/java/ref_string_startswith.asp
            if ( key.startsWith("#") || key.startsWith(" ") )  {

            // if ( key.charAt(0) == "#".charAt(0) || key.charAt(0) == " ".charAt(0) )  {
                thissim.println("\t\t  .....  skipping .... "+ key );
            }else {
            ///////////
              thissim.println(String.format( "running %s:  %s \t   type: %s ", whattodo, key, ktype) );
              switch (whattodo /*aka exo*/ ){
///////////< REPORTS :
                case "reports":
                if (CX[1]){ run_reports( key, ktype ) ; }
                //// Xreport.run_reports( String basename, String Type ) ;
                break;
///////////< SCENES :
                case "scenes":
                if (CX[2]){ run_scenes( key, ktype ); }
                //Xreport.run_scenes ( String basename, String Type ) ;
                break;
              }///EO switch 
            }  
        }
    echo_br();
}        
//////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////
public void save_plottab( String PLOTNAME ) {
  Simulation thissim = getActiveSimulation();
  String sep = System.getProperty("file.separator"); //get the right separator for your operative system     
  String CWDIR = thissim.getSessionDir() ;
  String SUBDIR = "otab" ;
  String SAVEDIR = CWDIR + sep + otab + sep ;
  String TABNAME = SAVEDIR + "tab_" +  PLOTNAME + ".csv";

  MonitorPlot monitorPlot_0 = 
    ((MonitorPlot) thissim.getPlotManager().getPlot( PLOTNAME ));
  monitorPlot_0.export(resolvePath( TABNAME ), ",");

}
//////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////
public Dictionary readtable( String csv_name, boolean[] EX ){	
    String sep = System.getProperty("file.separator"); 
    Dictionary<String, String> map  = new Hashtable<>() ;  
//    HashMap<String,String> map = new HashMap<String, String>();

    File csv_file = new File(csv_name);
    //public static void main(String[] args) throws ParseException, IOException {	        
    int[] REP = new int[50];
    REP[ 1] = 2 ; // repetitions
    Simulation thissim = getActiveSimulation();  
    thissim.println(String.format(
    "you are trying to read file: %s ", csv_name )
    );
    System.out.println(String.format(
    "you are trying to read file: %s ", csv_name )
    );
    try {
        ///// Import tables file
        Scanner import_table_csv = new Scanner( csv_file ) ; 
        import_table_csv.useDelimiter("\n");
        //// skip first couple lines of Headers
        for ( int nskip=0; nskip < REP[1]; ++nskip){
            import_table_csv.nextLine(); 
        }
        int linenr=0;
        while (import_table_csv.hasNextLine()) {
            linenr += 1;
            String s = import_table_csv.nextLine() ;

            if (EX[1]){
                echo_br();
                System.out.println(String.format(
                "[ Line #%5d  ] Reading.... \n%s",linenr, s)) ;
                thissim.println(String.format(
                "[ Line #%5d ] Reading.... \n%s",linenr, s)) ;
            }
            /// char a = "#".charAt(0) ;
            if ( s.charAt(0) != "#".charAt(0) || s.charAt(0) != " ".charAt(0) )  {
                String[] SREAD	= s.split(","); 
                map.put( SREAD[0], SREAD[1] );
            }
        }//EO: while ...
        import_table_csv.close();  /// closing file Scanner
    }//EO* try..*/ 
    catch (Exception e) {
                    thissim.println("error parsing file");
    } // EO try ..catch ...
    
    echo_br();

    return map;
}
//////////////////////////////////////////////////////////////////////////
   
//////////////////////////////////////////////////////////////////////////
public void echo_br( ){									  /// echo_br( ) ;
    Simulation thissim = getActiveSimulation();
        String bba = "-".repeat(72) ;
        System.out.println( bba ) ;
        thissim.println( bba ) ;
}
//////////////////////////////////////////////////////////////////////////



public void echo_bs( String basename, String savename){
/// echobs( basename, savename)
    Simulation thissim = getActiveSimulation();
    String sep = System.getProperty("file.separator"); 
    thissim.println(String.format(
     "  \t :: saving as %s ", basename, savename )) ;
        //" making ..... %s \t :: saving as %s ", basename, savename )) ;
    System.out.println(String.format(
     "  \t :: saving as %s ", basename, savename )) ;
}
//////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////

public void make_scenes_sa (Simulation thissim, String subdir, List<String> ListScenes ) {
//  Simulation thissim = getActiveSimulation();    
    String pretag="sce_" ;
    String sep = System.getProperty("file.separator"); 
    String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
    for ( String basename : ListScenes ) {
            String savename = CWDIR +subdir+sep + basename + ".png" ;
            echo_bs( basename, savename );
            Scene scene_0  = thissim.getSceneManager().getScene( basename ) ;
    //  scene_0.printAndWait(resolvePath( savename ), 1, 1024, 768, true, false);//  4:3
    //  scene_0.printAndWait(resolvePath( savename ), 1, 1280, 720, true, false);// 16:9
            scene_0.printAndWait(resolvePath( savename ), 1, 1600, 900, true, false);//  4:3
    }
    echo_br( ) ;
}///////////////////////////////////////////////////////////////////////////

public void make_scenes_3d (
            Simulation thissim, String subdir, List<String> ListScenes ) {

    String pretag="sce_" ;
    String sep = System.getProperty("file.separator"); 
    String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
    for ( String basename : ListScenes ) {
                // hardcopy_3dscene    ( basename ) ; ---------------------
                String savename = CWDIR +subdir+sep + basename + ".sce" ;
                echo_bs( basename, savename );
                Scene scene_4 = thissim.getSceneManager().getScene( basename );
                scene_4.export3DSceneFileAndWait(
                resolvePath(savename), basename, "", false, 
                SceneFileCompressionLevel.MEDIUM);
}
    echo_br( ) ;
}///////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////
public void hard_hist (
    Simulation thissim, 
    String subdir, List<String> List_Histograms) {
    String pretag="plot_" ;
    String sep = System.getProperty("file.separator"); 
    String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
    for ( String basename : List_Histograms ) {
                // hardcopy_hist( basename ) ; -----------------------
                String savename = CWDIR +subdir+sep +pretag+basename + ".png" ;
                echo_bs( basename, savename );
                HistogramPlot histogramPlot_0 = 
                    ((HistogramPlot) thissim.getPlotManager().getPlot(basename));
                histogramPlot_0.encode(resolvePath( savename ), "png", 1024, 768, true, false);
    }; 
    echo_br( ) ;

}
//////////////////////////////////////////////////////////////////////////

public void hard_plot( Simulation thissim, String subdir, List<String> ListPlots ) {
//		Simulation thissim = getActiveSimulation();    
    String pretag="plot_" ;
    String sep = System.getProperty("file.separator"); 
    String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;

    for ( String basename : ListPlots ) {
            //hardcopy_plot( basename,savename ) ; ---------------------------
            String savename = CWDIR +subdir+sep +pretag+basename + ".png" ;
            echo_bs( basename, savename );
            MonitorPlot monitorPlot_0 = 
                ((MonitorPlot) thissim.getPlotManager().getPlot( basename ));
            monitorPlot_0.encode(resolvePath( savename ), "png", 1024, 768, true, false);
}
echo_br( ) ;

}


//////////////////////////////////////////////////////////////////////////

public void save_sect ( Simulation thissim,  int endsect, 
    String fscalar, String dirs, String subdir ) {
 ////-------------------------------------------------------------------
    String pretag="sce_" ;
    String sep = System.getProperty("file.separator"); 
    String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
    String basename = fscalar + "_" + dirs ;
    String sectb    =           "B" + dirs ;
//    String subdir = CWDIR +"./spp/scn/" ;

for ( int sectv = 1; sectv <= endsect; sectv++ ) { 
        String pads  = (sectv < 10  ) ? "0" : "" ;
        String sects = pads + String.valueOf(sectv) ;
        String savename = CWDIR +subdir+sep + fscalar + "/" +basename +sects +".png" ;

    echo_bs( basename, savename );
    Units units_0 = 
    ((Units) thissim.getUnitsManager().getObject(""));

    ScalarGlobalParameter scalarGlobalParameter_0 = 
        ((ScalarGlobalParameter) thissim.get(GlobalParameterManager.class).getObject(sectb));
    scalarGlobalParameter_0.getQuantity().setUnits(units_0);
        scalarGlobalParameter_0.getQuantity().setValue(sectv);

        Scene scene_52 = thissim.getSceneManager().getScene(basename);
        scene_52.printAndWait(resolvePath( savename ), 1, 1000, 1000, true, false );

}
}

//////////////////////////////////////////////////////////////////////////

public void hardcopy_3dscene ( String basename, String subdir  ) {
    String pretag="sce_" ;
    Simulation thissim = getActiveSimulation();    
    String sep = System.getProperty("file.separator"); 
    String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;

    //    String subdir = CWDIR +"./spp/scn/" ;
    String savename = CWDIR +  subdir  + basename + ".sce" ;
        echo_bs( basename, savename );
    Scene scene_4 = thissim.getSceneManager().getScene( basename );
    scene_4.export3DSceneFileAndWait(
                resolvePath(savename), basename, "", false, 
                SceneFileCompressionLevel.MEDIUM);
    /*  
            SceneFileCompressionLevel.OFF,
            SceneFileCompressionLevel.LOSSLESS,
            SceneFileCompressionLevel.LOW, 
            SceneFileCompressionLevel.MEDIUM, 
            SceneFileCompressionLevel.HIGH, 
    */		
}
//////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
public void run_scenes ( String basename, String Type ) {
    String pretag="sce_" ;
    Simulation thissim = getActiveSimulation();
    String sep = System.getProperty("file.separator"); 
    String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
    String subdir = "post";
    switch ( Type ) {

    /////////////////////////////
        case "Plot" : 
            //thissim.println( "\t\t... doing hard_plot");
            make_plot(basename, subdir, thissim ) ;
            save_plottab( basename );
        break ; 
    /////////////////////////////
        case "Hist" :  
            //thissim.println( "\t\t... doing hard_hist");
            make_hist  (basename,  subdir, thissim ) ;
        break ; 
    /////////////////////////////
        case "Scene": 
            //thissim.println( "\t\t doing hard_scene");
            make_scene (basename,  subdir, thissim ) ;
        break ; 
    /////////////////////////////
        case "Sce3d" : 
            //thissim.println( "\t\t... doing hard_sce3d");
            //make_sce3d (basename,  subdir, thissim ) ;
        break ; 
    /////////////////////////////

    }///EOB switch
    //thissim.println( "    \t\t\t .... but not really");

  }//EOB public void run_scene /////////////////////////////////////////////

  //////////////////////////////////////////////////////////////////////////
  public void make_hist ( 
    String basename, String subdir, Simulation thissim  ) {
        String pretag="hist_" ;
        String sep = System.getProperty("file.separator"); 
        String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
            // hardcopy_hist( basename ) ; -----------------------
        String savename = CWDIR +subdir+sep +pretag+basename +".png" ;
        echo_bs( basename, savename );
        HistogramPlot histogramPlot_0 = 
            ((HistogramPlot) thissim.getPlotManager().getPlot(basename));
        histogramPlot_0.encode(resolvePath( savename ), "png", 1024, 768, true, false);
    echo_br( ) ;
  }/////////////////////////////////////////////////////////////////////////

  public void make_plot( 
    String basename, String subdir, Simulation thissim  ) {
    
        String pretag="plot_" ;
        String sep = System.getProperty("file.separator"); 
        String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
        
        //hardcopy_plot( basename,savename ) ; ---------------------------
        String savename = CWDIR +subdir+sep +pretag+basename +".png" ;
            echo_bs( basename, savename );
        MonitorPlot monitorPlot_0 = 
            ((MonitorPlot) thissim.getPlotManager().getPlot( basename ));
        monitorPlot_0.encode(resolvePath( savename ), "png", 1024, 768, true, false);
        echo_br( ) ;
  }/////////////////////////////////////////////////////////////////////////

  public void make_scene (
    String basename, String subdir, Simulation thissim  ) {
        String pretag="sce_" ;
        String sep = System.getProperty("file.separator"); 
        String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
        String savename = CWDIR +subdir+sep +pretag+basename +".png" ;
        echo_bs( basename, savename );
        Scene scene_0  = thissim.getSceneManager().getScene( basename ) ;
        //  scene_0.printAndWait(resolvePath( savename ), 1, 1024, 768, true, false);//  4:3
        //  scene_0.printAndWait(resolvePath( savename ), 1, 1280, 720, true, false);// 16:9
        scene_0.printAndWait(resolvePath( savename ), 1, 1600, 900, true, false);//  4:3
        echo_br( ) ;
  }/////////////////////////////////////////////////////////////////////////
  public void make_sce3d (
    String basename, String subdir, Simulation thissim  ) {
        String pretag="sce_" ;
        String sep = System.getProperty("file.separator"); 
        String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
        // hardcopy_3dscene    ( basename ) ; ---------------------
        String savename = CWDIR +subdir+sep +pretag+basename +".sce" ;
        echo_bs( basename, savename );
        Scene scene_4 = thissim.getSceneManager().getScene( basename );
        scene_4.export3DSceneFileAndWait(
        resolvePath(savename), basename, "", false, 
        SceneFileCompressionLevel.MEDIUM);
		echo_br( ) ;
  }/////////////////////////////////////////////////////////////////////////
  //private void make_sections (Simulation thissim, String subdir ) {
  private void make_sections (Simulation thissim, String subdir,int[] VectXYZ) {    
    /*
    // make_sections ( thissim,  subdir, VectXYZ) ;
     *  //Simulation thissim = getActiveSimulation();    
     *  //String subdir = "./spp/sect/" ;
     *  //int[] VectXYZ = [ 4, 13, 13 ] ;
     */
        
        String sep = System.getProperty("file.separator"); 
        String CWDIR = thissim.getSessionDir() + System.getProperty("file.separator") ;
        save_sect(thissim, 4, "tac"  , "X", subdir );echo_br();
        save_sect(thissim,13, "tac"  , "Y", subdir );echo_br();
        save_sect(thissim,13, "tac"  , "Z", subdir );echo_br();
        save_sect(thissim, 4, "vmag" , "X", subdir );echo_br();
        save_sect(thissim,13, "vmag" , "Y", subdir );echo_br();
        save_sect(thissim,13, "vmag" , "Z", subdir );echo_br();
  } 

  ///////////////////////////////////////////////////////////////////////////// */
////////////////////////////////////////////////////////////////////
 public void run_reports ( String ReportName, String Type ) {
    Simulation thissim = getActiveSimulation();
      switch (Type) {
        ///////////////////////////// 
        /*
          case "THIS_METHOD_REPORT":
            THIS_METHOD_REPORT Xreport  = ((THIS_METHOD_REPORT) 
              thissim.getReportManager().getReport(ReportName));
              Xreport.printReport(); break ;
             */
        /////////////////////////////
          case "Report":
            Report xr001  = ((Report) 
              thissim.getReportManager().getReport(ReportName));
              xr001.printReport(); break ;   
              
        /////////////////////////////
          case "ExpressionReport" :
            ExpressionReport xr002  = ((ExpressionReport) 
              thissim.getReportManager().getReport(ReportName));
              xr002.printReport(); break ; 
          
        /////////////////////////////
          case "MinReport" :
            MinReport xr003  = ((MinReport) 
              thissim.getReportManager().getReport(ReportName));
              xr003.printReport(); break ;   
        /////////////////////////////
          case "MaxReport" :
            MaxReport xr004  = ((MaxReport) 
              thissim.getReportManager().getReport(ReportName));
              xr004.printReport(); break ;   
  
        /////////////////////////////
          case "SumReport" :
            SumReport xr005  = ((SumReport) 
              thissim.getReportManager().getReport(ReportName));
              xr005.printReport(); break ;    
  
        /////////////////////////////
          case "ElementCountReport" :
            ElementCountReport xr006  = ((ElementCountReport) 
              thissim.getReportManager().getReport(ReportName));
              xr006.printReport(); break ; 
  
        /////////////////////////////
          case "MassFlowReport" :
            MassFlowReport xr007  = ((MassFlowReport) 
              thissim.getReportManager().getReport(ReportName));
              xr007.printReport(); break ;   
  
        /////////////////////////////
          case "MassFlowAverageReport" :
            MassFlowAverageReport xr008  = ((MassFlowAverageReport) 
              thissim.getReportManager().getReport(ReportName));
              xr008.printReport(); break ;   
  
        /////////////////////////////
        case "AreaAverageReport" :
          AreaAverageReport xr0091  = ((AreaAverageReport) 
          thissim.getReportManager().getReport(ReportName));
          xr0091.printReport(); break ;   

        /////////////////////////////
          case "MonitorIntegralReport" :
          MonitorIntegralReport xr0092  = ((MonitorIntegralReport) 
          thissim.getReportManager().getReport(ReportName));
          xr0092.printReport(); break ;   

        /////////////////////////////
          case "VolumeAverageReport" :
            VolumeAverageReport xr009  = ((VolumeAverageReport) 
              thissim.getReportManager().getReport(ReportName));
              xr009.printReport(); break ;   
  
        /////////////////////////////
          case "VolumeIntegralReport" :
            VolumeIntegralReport xr010  = ((VolumeIntegralReport) 
              thissim.getReportManager().getReport(ReportName));
              xr010.printReport(); break ;   
  
        /////////////////////////////
          case "SurfaceAverageReport" :
            AreaAverageReport xr011  = (( AreaAverageReport) 
              thissim.getReportManager().getReport(ReportName));
              xr011.printReport(); break ;   
  
        /////////////////////////////
          case "SurfaceIntegralReport" :
            SurfaceIntegralReport xr012  = ((SurfaceIntegralReport) 
              thissim.getReportManager().getReport(ReportName));
              xr012.printReport(); break ;   
              
        /////////////////////////////
          case "StatisticsReport" :
            StatisticsReport xr013  = ((StatisticsReport)       
              //// Used for statistical evluation of Monitors
              thissim.getReportManager().getReport(ReportName));
              xr013.printReport(); break ;   
  
        /////////////////////////////
          case "HeatTransferReport" :
            HeatTransferReport xr014  = ((HeatTransferReport)       
              //// Used for statistical evluation of Monitors
              thissim.getReportManager().getReport(ReportName));
              xr014.printReport(); break ;   
  
        /////////////////////////////
          case "CircuitElementCurrentReport" :  //BATTERY ELECTRIC
            CircuitElementCurrentReport xr015  = ((CircuitElementCurrentReport) 
              thissim.getReportManager().getReport(ReportName));
              xr015.printReport(); break ;   
  
        /////////////////////////////
          case "CircuitElementVoltageReport" : //BATTERY ELECTRIC
            CircuitElementVoltageReport xr016  = ((CircuitElementVoltageReport) 
              thissim.getReportManager().getReport(ReportName));
              xr016.printReport(); break ;   
  
        /////////////////////////////
          default:
            ExpressionReport Xreport  = ((ExpressionReport) 
              thissim.getReportManager().getReport(ReportName));
              Xreport.printReport(); break ; 
        
      }///EOB switch
  
    }//EOB public void run_report////////////////////////////////////////////
  

} 
////////   public class post_batch extends StarMacro  ////////////////////////
// Simcenter STAR-CCM+ macro 16.06.008																				
///////////////////////////////////////////////////////////////////////////// */

/*  REVISIONS ////////////////////////////////////////////////////////////////// 
 * PREV:    '2024-02-05-08:46U'
 * LAST:    '2024-02-22-16:57Z': +Reports MonitorIntegralReport, 
 * LAST:    '2024-02-22-17:39Z': +Reports MonitorIntegralReport, +TABPREF, +TABSUFF 
 * LAST:    '2024-04-13-14:01Z': +save_plottab ( basename )... 

*/  //////////////////////////////////////////////////////////////////////////// 

/*  FUTURE FEATURES //////////////////////////////////////////////////////////// 
    
    //// Execution Table ///-------------------------------------
    ///boolean[] QQ = new boolean[10]; 
    //int q1  = promptUserForInput(" enter '1' to run-report?  ", 0) ;
    //int q2  = promptUserForInput(" enter '2' to run-sceness? ", 0) ;
    String q1, q2 ; 
    BufferedReader bfn = new BufferedReader(
        new InputStreamReader(System.in));
    System.out.println(" enter '1' to run-report?  ") ;
    //String qs1 = bfn.readLine( ) ;
    q1 = reader.readLine() ; 
    //String q1  = Integer.parseInt( bfn.readLine() );
    System.out.println(" enter '2' to run-report?  ") ;
        //String qs2 = bfn.readLine( ) ;
    //int q2  = Integer.parseInt( bfn.readLine() );
    q2 = reader.readLine() ; 
    boolean qq1 = ( q1 =='1'?true:false ); 
    boolean qq2 = ( q2 =='2'?true:false ); 
    boolean[] QQ = { false, qq1, qq2 } ;    
    System.out.println( " QQ 1 " + QQ[1]) ;
    System.out.println( " QQ 1 " + QQ[2]) ;
    
///////////////////////////////////////////////////////////////////////////// */