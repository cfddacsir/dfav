/* /////////////////////////////////////////////////////////////////////////////
 * FILE:    tc_probes.java
 * TYPE:    starccm_java_macro   //{ Simcenter STAR-CCM+ macro 16.06.008 }//
 * PERS:    'Daniel.Collins@wisk.aero' 
 * LAST:    '2024-02-26-15:34Z': recapitualate... + if s.Startswith()... skip...
 * PURP:    'generate Reports, Plots and Scenes in STARCCM+ model based on
               keys listed in {TABPATH\reports.csv, TABPATH\scenes.csv} 
               where TABPATH is pathway specified in main class.

 * PREV:    '2023-10-18-T08:37-07:00':'adding REP[ ] to control extra loops of skiplines '
//////////////////////////////////////////////////////////////////////////////*/

/*
Simulation ActiveSim, boolean[] SWT,
 ActiveSim, SWT,
*/
package macro;
import star.common.*;
import star.base.neo.*;
import star.base.query.*;
import star.base.report.*;
import star.vis.*;
import star.common.Tag; 
import star.common.UserTag ; 

import star.meshing.*;

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
import java.util.Scanner;

//import javax.swing.*;
//import javax.swing.JFileChooser;

////////////////////////////////////////////////////////////////////////////////

public class tc_probes extends StarMacro {

  /////////////////////////////////////////////////////////////////////////////
  public void execute() {

//=============================================================================  
//# USER INPUTS --------------------------------------------------------------
    String INPUTFILE ;
     INPUTFILE = "G:\\My Drive\\mylab\\star\\probes\\" + "HG05_tcmap.csv";  
     //INPUTFILE = "G:\\My Drive\\mylab\\star\\probes\\out\\" + "HG05_tcmap.csv";  
    String filter_regcells ; //  = ""; // new String;
      filter_regcells = "Reg.CELLS"; // String filter_regcells = "reg_CELLS";
      filter_regcells = "TCREG";     // String filter_regcells = "reg_CELLS";

    boolean[] SWT = new boolean[50];
    int[] REP = new int[50];
    
    REP[ 1] = 2 ; // repetitions

    SWT[ 0] = false ; // do ALL 
    SWT[ 1] = true  ; // BatchProbes( INPUTFILE ) 
    SWT[ 5] = false ; // MakeGrouping() 
    SWT[ 3] = false ; // MakeTag() 
    SWT[ 6] = false ; // Groupreport

    SWT[20] = true  ; // SetName() 
    SWT[21] = true  ; // CreateProbe() 
    SWT[22] = false  ; // make_partsphere_as_tcprobe
    SWT[24] = false ; // make_surfacesection_for_tcprobe

    SWT[31] = false ; // MakeReportTemperatureBTS() 

//--<END USER INPUTS>----------------------------------------------------------
//=============================================================================
    String bbe = "=".repeat(72) ;
		String bba = "-".repeat(72) ;
    Simulation ActiveSim = getActiveSimulation();
  	ActiveSim.println( bbe ) ;
    System.out.println( bbe ) ;
	  if (SWT[ 5] || SWT[ 0] ){
          MakeGrouping( ActiveSim, SWT );
    }
	  if (SWT[ 3] || SWT[ 0] ){
          MakeTag( ActiveSim, SWT );
    }
	  if (SWT[ 6] || SWT[ 0] ){
          String GroupName =  "BTS_Temps"; 
          MakeGroupReport( ActiveSim, SWT, GroupName );
    }
    if (SWT[ 1] || SWT[ 0] ){
          BatchProbes(ActiveSim, SWT, INPUTFILE, filter_regcells, REP );
    }
  }
////////////////////////////////////////////////////////////////////////////////
  public void BatchProbes( 
      Simulation ActiveSim, 
      boolean[] SWT, 
      String INPUTFILE, 
      String filter_regcells,
      int[] REP
    ) {
		// Simulation ActiveSim = getActiveSimulation();
		// String INPUTFILE = "";
    // String filter_regcells = "Reg.CELLS"; // String filter_regcells = "reg_CELLS";
  	String csv_file = resolvePath(INPUTFILE); 
		File table_csv = new File(csv_file);
		String bbe= "=".repeat(72) ;
  	String bba= "-".repeat(72) ;
    ArrayList<double[]> vals = new ArrayList<double[]>();


		ActiveSim.println(String.format(
    "you are trying to read file: %s ", table_csv )
    );
		System.out.println(String.format(
    "you are trying to read file: %s ", table_csv )
    );
		try {
		  ///// Import tables file
  		Scanner import_table_csv = new Scanner( table_csv ) ; 
		  import_table_csv.useDelimiter("\n");
		  for ( int nskip=0; nskip < REP[1]; ++nskip){
      import_table_csv.nextLine(); // skip headers
      }
      int linenr=0;
			while (import_table_csv.hasNextLine()) {
 				linenr += 1;
		  	String s = import_table_csv.nextLine() ;
				System.out.println( bbe ) ;
				ActiveSim.println( bbe ) ;
        
				System.out.println(String.format(
				"[ Line #%5d ] Reading.... \n%s",linenr, s)) ;
				ActiveSim.println(String.format(
				"[ Line #%5d ] Reading.... \n%s",linenr, s)) ;
 
        String[] SREAD	= s.split(","); 
        if ( s.startsWith("#") || s.startsWith(" ") )  {          
            ActiveSim.println("\t\t  .....  skipping .... "+ s );
        }else {
          if (SWT[20  ] || SWT[ 0] ){
          ActiveSim.println(String.format(
            "[BatchPrboes]: test: %b --> DOING SetName() ", SWT[22] 
          )); 
          SetName( ActiveSim, SWT, SREAD,  filter_regcells ) ;
          }// SetName( ActiveSim, SWT, SREAD ) ;
        }

			}///EO while ...
      import_table_csv.close();  /// closing file Scanner
		} /*EO try..*/ 
		catch (Exception e) {
				ActiveSim.println("error parsing file");
		} // EO try ..catch ...
    //import_table_csv.close();  /// closing file Scanner
  	System.out.println( bbe ) ;
  	ActiveSim.println( bbe ) ;
  }//EOF BatchProbes()
  
////////////////////////////////////////////////////////////////////////////////
  public void SetName(
      Simulation ActiveSim, 
      boolean[] SWT, 
      String[] SREAD,  
      String filter_regcells 
    ) {
		// Simulation ActiveSim = getActiveSimulation();
    // String filter_regcells = ""; 
    // filter_regcells = "Reg.CELLS"; // String filter_regcells = "reg_CELLS";

    // Initialize strings and such...
    String TCSIG ;  //= 	"";
		String AKEY  ;  //= 	"";
		String BKEY  ;  //= 	"";
		String CKEY  ;  //=  "";
   
/*HG05_tcmap.csv ==
TCSIG,XPOS,YPOS,ZPOS,IGRP,TPOS,ICELL,CELLX,CELLY,MPOD,CPOD,SIDE,POLR
TC01,0.40445,-0.07232,0.10520,1,I,46,45,2,16,1,L,N
TC02,0.40445,0.02944,0.10520,1,J,46,45,2,16,1,L,N
*/
    TCSIG = 	"TC";
		AKEY  = 	"AK";
		BKEY  = 	"BK";
		CKEY  =   "CK";

/*
		TCSIG = 	String.parseString( SREAD[0] );
		AKEY  = 	String.parseString( SREAD[4] ); // IGRP
		BKEY  = 	String.parseString( SREAD[5] ); // TPOS 
		CKEY  =  String.parseString( SREAD[12] ); // 

*/
		int    ICELL     = Integer.parseInt(   SREAD[6] );
		double probePosX = Double.parseDouble( SREAD[1] ); // -0.000;
		double probePosY = Double.parseDouble( SREAD[2] )     -0.0085 +0.00315 ;		
		double probePosZ = Double.parseDouble( SREAD[3] ); // -0.000;
		TCSIG            = SREAD[0] ;
    
    ActiveSim.println(String.format(
				"[SetName]: Found Cell# %d ", ICELL )) ;

		String bba= "-".repeat(72);
		String Dasher  = "-";	
		String strCell = "";
		String strKA = "";
		String strKB = "";
		String strKC = "";
		String strTagA = "";
		String strTagB = "";
		String strTagC = "";
		String ProbeName= ""; 
		String ProbeGroup= ""; 
		String preICELL= "";
    double SETRADIUS = 15.0E-4 ; 
		preICELL = (ICELL < 10  ) ? "00" : 
							 (ICELL < 100 ) ? "0"  :	 "" ;
    strCell = preICELL + String.valueOf(ICELL) ; 

    ActiveSim.println(String.format(
       "[SetName]: test: %b ", SWT[22] )); 

    // --- strKey Names .....................................
		String	 preKeyX = ""; // "0" ;
		String	 preKeyY = ""; //BKEY <10 ? "0" : "" ;
		String	 preKeyZ = ""; //CKEY <10 ? "0" : "" ;
 		strKA =  preKeyX + String.valueOf(AKEY); // Grouping
 		strKB =  preKeyY + String.valueOf(BKEY); // x-z positioning on cell
 		strKC =  preKeyZ + String.valueOf(CKEY); // CellID 
    // .....................................................
		strTagA =  "TC"    + ""   ;
		strTagB =  "TC-G"  + "0" + strKA ;
		strTagC =  "tcsp"  + ""   ;
		//ProbeName = "CSIA" + strCell + Dasher 
		//									   + strKA +  strKB + strKC ;
		// ProbeName =  "Cell" + Dasher + strCell ;
    ProbeName  =  TCSIG ;
		ProbeGroup =  strTagA; // + "".concat(String.valueOf(AKEY));
/*
    */
  	// --- now call up and execute CreateProbe() ---->/**/
    ActiveSim.println(String.format(
     "[SetName]: test: %b ", SWT[22] )); 
    //if ( SWT[ 0] ||  SWT[22] || SWT[ 23 ] ){    
      ActiveSim.println(String.format(
        "[SetName]: test: %b --> DOING CreateProbe ", SWT[22] )); 
      if (SWT[ 21 ]  ){
        CreateProbe(
          ActiveSim, SWT,
          ProbeName, ProbeGroup, 
          strTagA, strTagB, strTagC , 
          probePosX, probePosY, probePosZ,
          filter_regcells
        );
      }
      if (SWT[ 22 ]  ){
        make_partsphere_as_tcprobe(
          ActiveSim, SWT,
          ProbeName, ProbeGroup, 
          strTagA, strTagB, strTagC , 
          probePosX, probePosY, probePosZ,
          filter_regcells,
          SETRADIUS
        );
      }
      if (SWT[ 23 ]  ){
        make_surfacesection_for_tcprobe(
          ActiveSim, SWT,
          ProbeName, ProbeGroup, 
          strTagA, strTagB, strTagC , 
          probePosX, probePosY, probePosZ,
          filter_regcells,
          SETRADIUS
        );
      }
    //}
    if (SWT[ 31 ] || SWT[ 0] ){      
          MakeReportTemperatureBTS( ActiveSim, SWT, ProbeName,  strCell );
    }
    

  } //EO public void SetName()

////////////////////////////////////////////////////////////////////////////////

public void make_partsphere_as_tcprobe(
    Simulation ActiveSim, boolean[] SWT,
    String ProbeName, String ProbeGroup, 
    String strTagA, String strTagB, String strTagC, 
    double probePosX, double probePosY, double probePosZ,
    String filter_regcells,
    double SETRADIUS 
    
  ) 
{
    //String filter_regcells = "reg_CELLS";
    String tag_TC = "TC" ;
    String group_probe = "TC";
    ProbeName = ProbeName + "sp" ; 
    //double SETRADIUS = 15.0E-4 ; 
    // Simulation ActiveSim = getActiveSimulation();

    ////// .... Defining Probe as SurfaceSection .....
    Units units_0 = 
        ActiveSim.getUnitsManager().getPreferredUnits(Dimensions.Builder().length(1).build());

    MeshPartFactory meshPartFactory_0 = 
        ActiveSim.get(MeshPartFactory.class);

    SimpleSpherePart simpleSpherePart_1 = 
        meshPartFactory_0.createNewSpherePart(ActiveSim.get(SimulationPartManager.class));
        simpleSpherePart_1.setDoNotRetessellate(true);
    //sphereSection_1.setPresentationName( ProbeName );
    simpleSpherePart_1.setPresentationName( ProbeName ); 
    LabCoordinateSystem labCoordinateSystem_0 = 
        ActiveSim.getCoordinateSystemManager().getLabCoordinateSystem();

    simpleSpherePart_1.setCoordinateSystem(labCoordinateSystem_0);
    simpleSpherePart_1.getOrigin().setCoordinateSystem(labCoordinateSystem_0);
    simpleSpherePart_1.getOrigin().setCoordinate( 
        units_0, units_0, units_0, new DoubleVector(
          new double[] {
            probePosX,probePosY,probePosZ 
          }
        )
      );

    simpleSpherePart_1.getRadius().setUnits(units_0);
    simpleSpherePart_1.getRadius().setValue(0.0015);
    simpleSpherePart_1.getRadius().setValue(SETRADIUS);

    //simpleSpherePart_1.getTessellationDensityOption().setSelected(TessellationDensityOption.Type.MEDIUM);
    simpleSpherePart_1.getTessellationDensityOption().setSelected(TessellationDensityOption.Type.FINE  );
    //simpleSpherePart_1.getTessellationDensityOption().setSelected(TessellationDensityOption.Type.VERY_FINE );

    simpleSpherePart_1.rebuildSimpleShapePart();
    simpleSpherePart_1.setDoNotRetessellate(false);

    /// OPTIONAL set tags
    if ( SWT[11] ) {
      UserTag userTag_0 = 
        ((UserTag) ActiveSim.get(TagManager.class).getObject( strTagA ));
      UserTag userTag_1 = 
        ((UserTag) ActiveSim.get(TagManager.class).getObject( strTagB ));

      ActiveSim.get(TagManager.class).setTags (simpleSpherePart_1, new NeoObjectVector(new Object[] {userTag_0, userTag_1}));
    }


}// EO   private void CreateProbe(....)
//////////////////////////////////////////////////////////////////////////////// 
////////////////////////////////////////////////////////////////////////////////

public void make_surfacesection_for_tcprobe(
    Simulation ActiveSim, boolean[] SWT,
    String ProbeName, String ProbeGroup, 
    String strTagA, String strTagB, String strTagC, 
    double probePosX, double probePosY, double probePosZ,
    String filter_regcells,
    double SETRADIUS
  ) 
{
//String filter_regcells = "reg_CELLS";
String tag_TC = "TC" ;
String group_probe = "TC";
ProbeName = ProbeName + "ssdp" ; 
// double SETRADIUS = 15.0E-4 ; 
// Simulation ActiveSim = getActiveSimulation();

////// .... Defining Probe as SurfaceSection .....
  SphereSection sphereSection_1 = 
      (SphereSection) ActiveSim.getPartManager().createImplicitPart(new NeoObjectVector(new Object[] {}), 1.0, new DoubleVector(new double[] {0.0, 0.0, 0.0}), 0, 1, new DoubleVector(new double[] {0.0}), null);
    sphereSection_1.setPresentationName( ProbeName );

    Units units_0 = ((Units) ActiveSim.getUnitsManager().getObject("m")) ;

    sphereSection_1.getOriginCoordinate().setCoordinate( 
          units_0, units_0, units_0, 
            new DoubleVector(
              new double[] { probePosX, probePosY, probePosZ } 
            )
          );
    sphereSection_1.getRadius().setValueAndUnits( 5.0E-4, units_0);
    sphereSection_1.getRadius().setValueAndUnits( SETRADIUS , units_0);

    QueryFilter queryFilter_0 = 
      ((QueryFilter) ActiveSim.get(QueryFilterManager.class).getObject("Reg.CELLS"));
    QueryFilter queryFilter_1 = 
      ((QueryFilter) ActiveSim.get(QueryFilterManager.class).getObject("Reg.TABS"));
    QueryFilter queryFilter_2 = 
      ((QueryFilter) ActiveSim.get(QueryFilterManager.class).getObject("Reg.BUSBAR"));

    sphereSection_1.getInputParts().setQuery( 
        new Query(
          new CompoundPredicate( 
              CompoundOperator.Or, 
              Arrays.<QueryPredicate>asList( 
                  new QueryFilterPredicate(  
                    QueryFilterOperator.Matches, queryFilter_0), 
                  new QueryFilterPredicate( 
                    QueryFilterOperator.Matches, queryFilter_1), 
                  new QueryFilterPredicate(
                    QueryFilterOperator.Matches, queryFilter_2)
                  )
              ), 
        Query.STANDARD_MODIFIERS)
      );
    /// OPTIONAL set tags
    if ( SWT[11] ) {
      //UserTag userTag_0 = 
      //  ((UserTag) ActiveSim.get(TagManager.class).getObject("TC"));
      UserTag userTag_0 = 
        ((UserTag) ActiveSim.get(TagManager.class).getObject( strTagA ));
      //UserTag userTag_1 = 
      //  ((UserTag) ActiveSim.get(TagManager.class).getObject("TC-G01"));
      UserTag userTag_1 = 
        ((UserTag) ActiveSim.get(TagManager.class).getObject( strTagB ));

      ActiveSim.get(TagManager.class).setTags(sphereSection_1, new NeoObjectVector(new Object[] {userTag_0, userTag_1}));
    }


}// EO   private void CreateProbe(....)
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
  public void CreateProbe(
      Simulation ActiveSim, boolean[] SWT,
			String ProbeName, String ProbeGroup, 
			String strTagA, String strTagB, String strTagC, 
			double probePosX, double probePosY, double probePosZ,
      String filter_regcells
    ) 
  {
    //String filter_regcells = "reg_CELLS";
    ProbeName = ProbeName + "pt" ; 
    String tag_TC = "TC" ;
    String group_probe = "TC";
    // Simulation ActiveSim = getActiveSimulation();

	////// .... Defining PointPart .....
    PointPart pointPart_1 = 
      ActiveSim.getPartManager().createPointPart(new NeoObjectVector(new Object[] {}), new DoubleVector(new double[] {0.0, 0.0, 0.0}));

    pointPart_1.setPresentationName( ProbeName );
    Units units_0 = 
      ((Units) ActiveSim.getUnitsManager().getObject("m"));
    pointPart_1.getPointCoordinate().setCoordinate(units_0, units_0, units_0, new DoubleVector(new double[] {probePosX, probePosY, probePosZ }));

	////// ....  applying Parts from Filter reg_CELLS
    QueryFilter queryFilter_12 = 
      ((QueryFilter) ActiveSim.get(QueryFilterManager.class).getObject(filter_regcells));
    pointPart_1.getInputParts().setQuery(new Query(new QueryFilterPredicate(QueryFilterOperator.Matches, queryFilter_12), Query.STANDARD_MODIFIERS));



  }// EO   private void CreateProbe(....)
////////////////////////////////////////////////////////////////////////////////

  public void MakeGrouping (
      Simulation ActiveSim, 
      boolean[] SWT 
    ){

    String group_probe = "tc_probes";
    // String[] tag_groups = { "X01", "X02", "X03", "X04" };
    List<String> tag_groups = Arrays.asList( 
          "X01", "X02", "X03", "X04" 
		);

    // Simulation ActiveSim = getActiveSimulation();

    ActiveSim.getPartManager().getGroupsManager().createGroup("New Group");
    ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject("New Group")).setPresentationName(group_probe);

/*		String savename = CWDIR + subdir + basename + ".png" ;
 */
 
    for ( String tag : tag_groups ) {

      ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().createGroup("New Group");
      ((ClientServerObjectGroup) ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().getObject("New Group")).setPresentationName(tag);

    }

  } //EO private void MakeGrouping ()   
////////////////////////////////////////////////////////////////////////////////

/*

  public void MakeGrouping_1 (Simulation ActiveSim, boolean[] SWT ) {

    String group_probe = "csia-probes";
    // String[] tag_groups = { "X01", "X02", "X03", "X04" };
    List<String> tag_groups = Arrays.asList( 
          "X01", "X02", "X03", "X04" 
		);

    // Simulation ActiveSim = getActiveSimulation();

    ActiveSim.getPartManager().getGroupsManager().createGroup("New Group");

    ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject("New Group")).setPresentationName(group_probe);

    ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().createGroup("New Group");

    ((ClientServerObjectGroup) ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().getObject("New Group")).setPresentationName("X04");

    ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().createGroup("New Group");

    ((ClientServerObjectGroup) ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().getObject("New Group")).setPresentationName("X03");

    ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().createGroup("New Group");

    ((ClientServerObjectGroup) ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().getObject("New Group")).setPresentationName("X02");

    ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().createGroup("New Group");

    ((ClientServerObjectGroup) ((ClientServerObjectGroup) ActiveSim.getPartManager().getGroupsManager().getObject(group_probe)).getGroupsManager().getObject("New Group")).setPresentationName("X01");

  } //EO private void make_grouping ()   
  
*/
////////////////////////////////////////////////////////////////////////////////

  public void MakeTag( 
      Simulation ActiveSim, 
      boolean[] SWT 
    ) {
    // Simulation ActiveSim = getActiveSimulation();
    UserTag userTag_0 = 
      ActiveSim.get(TagManager.class).createNewUserTag("CSIA-Probe");
		String strTagA = "";		String strTagB = "";		String strTagC = "";
		String strDir; String strKey; String strTag ; String preKey;
    for ( int IKEY = 1; IKEY < 5 ; IKEY++ ){
      strDir =  "I";
			preKey =  "0" ;
		  strTag =  "CSIA-" + strDir + preKey + String.valueOf(IKEY) ;
    	UserTag userTag_1 = 
      	ActiveSim.get(TagManager.class).createNewUserTag( strTag );
		}       
    for ( int IKEY = 1; IKEY < 14 ; IKEY++ ){
      strDir =  "J";
			preKey = IKEY <10 ? "0" : "" ;
		  strTag =  "CSIA-" + strDir + preKey + String.valueOf(IKEY) ;
    	UserTag userTag_1 = 
      	ActiveSim.get(TagManager.class).createNewUserTag( strTag );
		}       
    for ( int IKEY = 1; IKEY < 14 ; IKEY++ ){
      strDir =  "K";
			preKey = IKEY <10 ? "0" : "" ;
		  strTag =  "CSIA-" + strDir + preKey + String.valueOf(IKEY) ;
    	UserTag userTag_1 = 
      	ActiveSim.get(TagManager.class).createNewUserTag( strTag );
		}       
  } //EO private void MakeTag()
////////////////////////////////////////////////////////////////////////////////
  public void MakeReportTemperatureBTS(
      Simulation ActiveSim, 
      boolean[] SWT,
      String ProbeName, 
      String strCell 
    ) {
    // "BTS_011"  = new String ReportName
    // "CSIA-011" = ProbeName 
    String ReportName = "BTS_" + strCell ; 
      // Simulation ActiveSim = getActiveSimulation();

    SumReport sumReport_1 = 
      ActiveSim.getReportManager().createReport(SumReport.class);

    sumReport_1.setPresentationName(ReportName);

    PrimitiveFieldFunction primitiveFieldFunction_0 = 
      ((PrimitiveFieldFunction) ActiveSim.getFieldFunctionManager().getFunction("Temperature"));

    sumReport_1.setFieldFunction(primitiveFieldFunction_0);

    Units units_0 = 
      ((Units) ActiveSim.getUnitsManager().getObject("C"));

    sumReport_1.setUnits(units_0);

    sumReport_1.getParts().setQuery(null);

    PointPart pointPart_1 = 
      ((PointPart) ActiveSim.getPartManager().getObject(ProbeName));

    sumReport_1.getParts().setObjects(pointPart_1);

    sumReport_1.printReport();
		////// .... Moving into Group
    ((ClientServerObjectGroup) ActiveSim.getReportManager().getGroupsManager().getObject("TC_Temps")).getGroupsManager().groupObjects("TC_Temps", new NeoObjectVector(new Object[] {sumReport_1}), true);


  } //EO private void MakeReportTemperatureBTS(String ProbeName, String strCell )
////////////////////////////////////////////////////////////////////////////////
  public void MakeGroupReport( 
      Simulation ActiveSim, 
      boolean[] SWT, 
      String GroupName 
    ) {
    // String GroupName =  "BTS_Temps"; 
    // Simulation ActiveSim = getActiveSimulation();
    ActiveSim.getReportManager().getGroupsManager().createGroup("New Group");
    ((ClientServerObjectGroup) ActiveSim.getReportManager().getGroupsManager().getObject("New Group")).setPresentationName(GroupName);
/*
    SumReport sumReport_1 = 
      ((SumReport) ActiveSim.getReportManager().getReport("BTS_011"));
    ((ClientServerObjectGroup) ActiveSim.getReportManager().getGroupsManager().getObject("BTS_Temps")).getGroupsManager().groupObjects("BTS_Temps", new NeoObjectVector(new Object[] {sumReport_1}), true);
*/
  }
// ..........................................................................//

} //EO public class csiapos_auto extends StarMacro {

//#############################################################################
///////////////////////////////////////////////////////////////////////////////
//import javax.swing.*;
//import javax.swing.JFileChooser;
		/*  ////  
			  ___ List Variables ___
				String strCell ,
				String strKA ,
				String strKB ,
				String strKC ,
				String ProbeName,
				String strTagA ,
				String strTagB ,
				String strTagC ,
				double probePosX ,
				double probePosY ,
				double probePosZ
		*/
		/*
    int 	 	ICELL = 1;
  	int 		AKEY = 1;
  	int 		BKEY = 4;
	  int 		CKEY = 1;
  	double 	probePosX = 1.663078;
  	double 	probePosY = 0.565530;
  	double 	probePosZ = 0.235678;
		*/

		/*
		System.out.println(
    "=================================: "+"\n"+
	  " the values that were entered " 		+"\n"+
		" ProbeName  : " + ProbeName +"\n"+
    "---------------------------------: "+"\n"+
   	" icell : " + strCell +"\n"+
		" xkey  : " + strKA +"\n"+
		" ykey  : " + strKB +"\n"+
		" zkey  : " + strKC +"\n"+
		" xtag  : " + strTagA +"\n"+
		" ytag  : " + strTagB +"\n"+
		" ztag  : " + strTagC +"\n"+
		" xpos  : " + probePosX +"\n"+
		" ypos  : " + probePosY +"\n"+
		" zpos  : " + probePosZ +"\n"+
    "=================================: "+"\n"
		);
		*/
			/* 
 				System.out.println("   Bit 0: " + SREAD[0] 					) ;
 				System.out.println("   Bit 1: " + SREAD[1]  				) ;
 				System.out.println("   Bit 2: " + SREAD[2] 					) ;
 				System.out.println("   Bit 3: " + SREAD[3]  				) ;
 				System.out.println("   Bit 4: " + SREAD[4] 					) ;
 				System.out.println("   Bit 5: " + SREAD[5]  				) ;
 				System.out.println("   Bit 6: " + SREAD[6]  				) ;
			*/
////////////////////////////////////////////////////////////////////////////////


//#############################################################################
/* FOOTER / VERSIONING ////////////////////////////////////////////////////////
 
_PREV:{
          '2023-10-11-T12:20-07:00': '',     
          '2023-10-13-T17:02-07:00': '',     
          '2023-10-16-T06:17-07:00': '',     
          '2023-10-16-T08:41-07:00': '',
          '2023-10-17-T13:54-07:00': 'tc_probes__NqbT1354.java',
   }
 );
// 
// Simcenter STAR-CCM+ macro:
// Written by Simcenter STAR-CCM+ 16.06.008
*/
//#############################################################################

//#############################################################################
/* NOTES 
 * 
 * 
 * 
 */

//#############################################################################
