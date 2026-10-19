
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings
# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from scipy import stats
# %matplotlib inline
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score;
from sklearn.model_selection import cross_val_predict;
from sklearn.preprocessing import PolynomialFeatures;
from sklearn.linear_model import Ridge ;
from sklearn.model_selection import GridSearchCV;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import myfavs as my;

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hr = 60*'==';
br = 60*'--';
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def pbr(i=1,n=60,):
    symbols= '''#=-~''';
    br = n*symbols[i] ;
    print (br);
    return br;

def pbs(i=0,n=60,prefix="# "):
    prefix = "" + ""*(prefix==None)
    symbols = [chr(i) for i in range(32, 64) ];
    br = prefix + (n-len(prefix))*symbols[i] ;
    print (br);
    return br;

def alphabet():
    alphabet = [chr(i) for i in range(65, 65+26) ]
    return alphabet;

def smybols():
    alphabet = [chr(i) for i in range(32, 64) ]
    return alphabet;
    
def whoami( x ):
    print( type( x) )
    #if type(x) == 
    print( )
    return None;

######################################################################
def tcenter( s, spad="#",sp = " ",n=60):
    e = (int(n/2) - int((len(s)+len(sp))/2) )//len(spad);
    return str( (e)*spad + (sp)+(s)+(sp) +(e)*spad) ;

def reportaction( action, do=True ):
    print( tcenter( action,n=80,sp="  ") );
    if do:
     eval( 'print( {} ) '.format( action ));
    print( tcenter( "#",n=80,sp="") );
######################################################################
# made special for reporting df characterisitics:dfcharacter(df) ----
def dfcharacter( df ):
    do=True;
    Lactions=[
        'df.shape',
        'df.columns',
        'df.head()',
        'df.info()',
        'df.describe()',
        'df.corr()',
        'my.report_missing(df)'
    ]
    for action in ( Lactions ):
        #reportaction( h, do =False );
        print( tcenter( action,n=80,sp="  ") );
        #if do:
        eval( 'print( {} ) '.format( action ));
        print( tcenter( "#",n=80,sp="") );

######################################################################

######################################################################

######################################################################
# WRANGLE AND CLEAN
######################################################################
##  test for missing
def missing(df):
    missing_data = df.isnull();
    print( missing_data.head(5) );
    for column in missing_data.columns.values.tolist():
        print(column);
        print (missing_data[column].value_counts());
        print("") ;
def report_missing( df ):
    missing_data = df.isnull() ;
    #missing_data.head(5) 
    report=list();
    for column in missing_data.columns.values.tolist():
        ct = missing_data[column].value_counts()[0] ;
        gr = missing_data[column].shape[0] ;
        null = gr - ct;
        report.append( [ column, ct, null, gr ] );
        #print (missing_data[column].value_counts())
        #print("")  
    rp = pd.DataFrame( data=report, index=None, columns=['col','nonull','Nulls', 'Size']);
    return rp;

# Cleaning
## replace duds 
def cleanval( df ):
    s = '?'
    df.replace( s, np.nan, inplace=True);
    return df;

## repalce with mean
def replacemean(df, xlab ):
    pass   
    mu = df[ xlab ].astype("float").mean(axis=0);
    #mu
    df[ xlab ].replace( np.nan, mu, inplace=True) ;
    return df;

## replace with top frequent
def replacefreq( df, xlab, show=True, replace=True) :
    x1  = df[ xlab ].value_counts();
    top = vct = df[ xlab ].value_counts().idxmax(); 
    #print( "counts ", x1, "idmax: ", x2 )
    #top = vct
    if show: print ("top count: ", top)
    if replace: df[ xlab ].replace( np.nan, top, inplace=True);
    return df ;

def dfhints():
    hints=['shape','info()','describe()','corr()']
    for h in hints:
        pass;
    return None;
### C07-M03 

def pccPlot1( feature, target, df, splot=True ):
    ''' produces Pearson Coefficient & P-value and a regression plot for Feature and Target in Dataframe df
    '''
    pf = "| {:20s} | {:20s} | {:15s} | {:15s} |";
    hr = 50*'=='; br = 50*'--';
    pearson_coef, P_value = stats.pearsonr(df[feature], df[target]);
    #print("feature of {:30s} :\t PPC : {}. PPv : {} ".format( feature, pearson_coef, P_value ));
    print( hr );
    print(" Pearson Correlation Coefficient and P-value");
    print( pf.format( "FEATURE", "TARGET" , "PearsonCorr" , "P-value" ))
    print( pf.format( feature, target, f'{pearson_coef:+8.7f}', f'{P_value:8.5e}' ))
    print( br );
    if splot: sns.regplot(x=feature, y=target, data=df) ; plt.show();

def pccPlot( feature, target, df, splot=True ):
    ''' produces Pearson Coefficient & P-value and a regression plot for Feature and Target in Dataframe df
    '''
    pf = "| {:20s} | {:20s} | {:15s} | {:15s} |";
    hr = 83*'='; br = 83*'-';
    pearson_coef, P_value = stats.pearsonr(df[feature], df[target]);
    #print("feature of {:30s} :\t PPC : {}. PPv : {} ".format( feature, pearson_coef, P_value ));
    print( hr );
    print("| Pearson Correlation Coefficient and P-value |");
    print( pf.format( "FEATURE", "TARGET" , "PearsonCorr" , "P-value" ))
    print( pf.format( feature, target, f'{pearson_coef:+8.7f}', f'{P_value:8.5f}' ))
    print( br );
    if splot: sns.regplot(x=feature, y=target, data=df) ; plt.show();
    
def m():
    # Correlation values of the three attributes with Price
    for feature in [ "CPU_frequency", "Screen_Size_inch" , "Weight_pounds" ]:
        pccPlot( feature, "Price", df, splot=False)

def BoxPlot( feature, target, df ):
    print( br );
    sns.boxplot(x=feature, y=target, data=df) ; plt.show();
    print( df.corr() );

def headsandtails( df):
    print ( df.shape );
    print ( df.head(5));
    print ( df.tail(5));
# GROUPBY AND PIVOT
def group_and_pivot():
    sample = df [ ["GPU", "CPU_core", "Price"] ]
    dfgrp = sample.groupby( ["GPU", "CPU_core"], as_index=False).mean()
    dfgrp
    
    grouped_pivot = dfgrp.pivot( index="GPU", columns="CPU_core")
    grouped_pivot
    
    # grouped_pivot = dfpivot ;
    fig, ax = plt.subplots()
    im = ax.pcolor(grouped_pivot, cmap='RdBu')
    
    #label names
    row_labels = grouped_pivot.columns.levels[1]
    col_labels = grouped_pivot.index
    
    #move ticks and labels to the center
    ax.set_xticks(np.arange(grouped_pivot.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(grouped_pivot.shape[0]) + 0.5, minor=False)
    
    #insert labels
    ax.set_xticklabels(row_labels, minor=False)
    ax.set_yticklabels(col_labels, minor=False)
    
    fig.colorbar(im)
    
    plt.show();

    # import matplotlib as mpl
    # Write your code below and press Shift+Enter to execute
    # Create the Plot
    cmap1 = mpl.colors.Colormap('RdBu')
    #rev = cmap1.reversed()
    #plt.pcolor( dfpivot, cmap='RdBu', )
    plt.pcolor( grouped_pivot, cmap='RdBu_r', )
    plt.title(" Price as factor of GPU and CPU_core")
    plt.xlabel("GPU")
    plt.ylabel("CPU")
    plt.colorbar()
    plt.show()


## C07.M05 MODEL EVALUATION, TRAINING AND REGRESSION

def cols_not_target( target, df):
    xparms = list(); 
    for c in df.columns:
        if c != target: xparms.append(c);
    return xparms;

def datapairs( target, df ):
    feature = [ c for c in df.columns if c!=target ]
    Z = df[ feature ]
    Y = df[ target ]
    return Y, Z;


def linearmodel_single( X, Y, df):
    #target='Charges';
    #feature='Smoker';
    #X = df [[feature]]; 
    #Y = df [target] ;
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler, PolynomialFeatures
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import mean_squared_error, r2_score
    lr = LinearRegression()
    lr.fit ( X, Y)
    Yhat = lr.predict(X)
    mse_slr = mean_squared_error( Y , Yhat)
    rs = lr.score(X, Y)
    print( f'The R-square for Linear Regression is: {rs}')
    print( f'The mean square error of price and predicted value is: ', mse_slr)

def linearRegSingleFeature( feature1, target, df ):
    from sklearn.linear_model import LinearRegression
    X = df[[feature1]].astype(float);
    Y = df[target];
    lr = LinearRegression();lr.fit(X,Y);
    pbr(2);
    rs = lr.score(X, Y);print("R2 - linear regression predicting *{target}* using feature *{feature1}* :", rs); 
    pbr(1);
    return rs;

'''
Course07-Graded-Question
'''
def linearRegMultipleFeatures( features, target, df ):
    from sklearn.linear_model import LinearRegression
    Y = df[target];
    X = df[features].astype(float);
    lr = LinearRegression();lr.fit(X,Y);
    yhat = lr.predict( X );
    rs = r2_score(Y, yhat );
    pbr(1);
    print(f"Linear regression, predicting *{target}* from multiple **features** "); print("<", end="");
    for f in features: print(f"{f}, ", sep='', end='');
    print(">\n", end="");print(f" R2 score : {rs}"); 
    pbr(1);
'''
Question 8:
target = "price" ;"⟶"
Z = df [features]
Z = Z.astype(float);
Y = df[ target ];
pipe=Pipeline (Input);
pipe.fit(Z,Y);
targetipe=pipe.predict(Z);
rs = (r2_score(Y,targetipe));
#features = Z.columns; Y.columns;
print(f"Pipeline regression, predicting *{target}* from multiple features "); print(" <", end="");
for f in features: print(f"{f}, ", sep='', end='');
print(">\n", end="");print(f" ⟶ R2 score : {rs}");
'''
def pipeline_features( features, target, df, Input=None ):
    from sklearn.preprocessing import PolynomialFeatures 
    from sklearn.linear_model import LinearRegression 
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline 
    #Pipeline Constructor
    if Input==None:
      Input=[ 
        ('polynomial', PolynomialFeatures(include_bias=False)),
        ('scale' ,     StandardScaler()),
        ('model',      LinearRegression()) 
    ];
    # Pipeline constructor 
    XX = df [features].astype(float); Y = df[ target ];
    pipe = Pipeline (Input);
    pipe.fit(XX,Y);
    ypipe =pipe.predict(XX);
    rs = (r2_score(Y, ypipe ));
    print(f"Pipeline regression, predicting *{target}*from multiple features "); print("<", end="");
    for f in features: print(f"{f}, ", sep='', end='');
    print(">\n", end="");print(f" R2 score : {rs}");
    return rs; 
    


def model_split( x_data, y_data, split=0.3 ):
    # Model splitting
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = \
      train_test_split(x_data, y_data, test_size=0.3,
      random_state=0);
    return x_train, x_test, y_train, y_test ;

def model_split_features( features, target, df, split=0.3 ):
    # Model splitting
    from sklearn.model_selection import train_test_split
    X = x_data = df[ features ]
    Y = y_data = df[ target ]
    x_train, x_test, y_train, y_test = \
      train_test_split( X , Y , test_size=split,
      random_state=0);
    return x_train, x_test, y_train, y_test ;

def cross_validation( x_data, y_data ):
    # Cross_validation
    from sklearn.model_selection import cross_val_score;
    lr = LinearRegression() ;
    score = cross_val_score(lr, x_data, y_data, cv=3) ;  ## score<np.arr>
    yhat  = cross_val_predict(lr, x_data, y_data, cv=3); ## yhat<np.arr>


def polytesting( x_test, x_train, y_test, y_train, feature='col' ):
    # Over-fitting
    #feature = 'horsepower'
    Rsq = list() ;
    order = [1,2,3,4] ;
    for n in order:
        pr = PolynomialFeatures(degree=n) ;
        lr = LinearRegression() ;
        x_train_pr = pr.fit_transform(x_train[[ feature ]]) ;
        x_test_pr = pr.fit_transform(x_test[[ feature ]]) ;
        lr.fit(x_train_pr,y_train) ;
        Rsq.append(lr.score(x_test_pr,y_test)) ;
    RsqDf = pd.DataFrame( Rsq )
    return RsqDf;
    
def plot_polytest( Rsq ):
    plt.scatter( x=Rsq[0], y=Rsq[1] ) ; 
    #plt.plot( order, Rsq[1]);
    plt.ylabel(' R2 value ');
    plt.xlabel(' poly order ');
    plt.show();

def RidgeRegress( features, target, df, testsplit=0.3 ):
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import train_test_split
    X = df[features];
    Y = df[ target ];
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=1);
    print("number of test samples:", x_test.shape[0]);
    print("number of training samples:",x_train.shape[0]);
    from sklearn.linear_model import Ridge;
    RidgeModel = Ridge(alpha=0.1);
    RidgeModel.fit( x_train, y_train );
    Yhat = RidgeModel.predict( x_test );
    rs = r2_score( y_test, Yhat ) ;
    pbr(1);
    print( f"R2 score from Ridge Regression : {rs}"); 
    pbr(1);
    return rs;
    
def gridsearch_example( x_data, y_data, ):
    from sklearn.linear_model import Ridge ;
    from sklearn.model_selection import GridSearchCV;
    parameters1= [{'alpha': [0.001,0.1,1, 10, 100, 1000,10000,100000,100000] } ];
    RR=Ridge ();
    Grid = GridSearchCV(RR, parameters1, cv=4) ;
    Grid.fit( x_data , y_data ) ;
    Grid.best_estimator_ ;
    Scores = Grid.cv_results_scores ['mean_test_score'];


#################################################################################
if '__main__'==__name__: ## for testing purposes
 pass;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 if 0: ## TEST SAMPLE
    import sample_df;
    df = sample_df.sample_df();    
    print ( type (df))
    #my.dfcharacter(df);
    print( df.head() );
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 if 1: ## testing dfcharacter(df)
    import sample_df;
    df = sample_df.sample_df();
    dfcharacter(df);
#################################################################################
