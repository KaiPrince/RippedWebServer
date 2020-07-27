module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Json.Decode as D
import Json.Encode as E



-- MAIN


main : Program E.Value Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = \_ -> Sub.none
        }



-- MODEL


type alias Model =
    { fileName : String
    , content : String
    , filePath : String
    , editable : Bool
    , uploadedBy : String
    , uploadedAt : String
    }



-- Here we use "flags" to load information in from localStorage. The
-- data comes in as a JS value, so we define a `decoder` at the bottom
-- of this file to turn it into an Elm value.
--
-- Check out index.html to see the corresponding code on the JS side.
--


init : E.Value -> ( Model, Cmd Msg )
init flags =
    ( case D.decodeValue decoder flags of
        Ok model ->
            model

        Err _ ->
            { fileName = "", content = "", filePath = "", editable = False, uploadedBy = "", uploadedAt = "" }
    , Cmd.none
    )



-- UPDATE


type Msg
    = FileNameChanged String


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FileNameChanged fileName ->
            ( { model | fileName = fileName }
            , Cmd.none
            )



-- VIEW


view : Model -> Html Msg
view model =
    div []
        [ Html.form
            [ method "POST"
            , enctype "multipart/form-data"
            ]
            [ div [ class "form-group row" ]
                [ label
                    [ for "file_name", class "col-sm-2 col-form-label" ]
                    [ text "Title" ]
                , div [ class "col-sm-10" ]
                    [ input
                        [ id "file_name"
                        , name "file_name"
                        , type_ "text"
                        , class
                            (if model.editable then
                                "form-control"

                             else
                                "form-control-plaintext"
                            )
                        , readonly (not model.editable)
                        , placeholder "Shopping list"
                        , onInput FileNameChanged
                        , value model.fileName
                        ]
                        []
                    ]
                ]
            , if model.filePath /= "" then
                div [ class "form-group row" ]
                    [ label [ for "file-path", class "col-sm-2 col-form-label" ] [ text "File Name" ]
                    , div [ class "col-sm-10" ]
                        [ input [ type_ "text", readonly True, class "form-control-plaintext", value model.filePath ] []
                        ]
                    ]

              else
                div [] []
            , if model.uploadedBy /= "" then
                div [ class "form-group row" ]
                    [ label [ for "file-path", class "col-sm-2 col-form-label" ] [ text "Uploaded By" ]
                    , div [ class "col-sm-10" ]
                        [ input [ type_ "text", readonly True, class "form-control-plaintext", value model.uploadedBy ] []
                        ]
                    ]

              else
                div [] []
            , if model.uploadedAt /= "" then
                div [ class "form-group row" ]
                    [ label [ for "file-path", class "col-sm-2 col-form-label" ] [ text "Uploaded At" ]
                    , div [ class "col-sm-10" ]
                        [ input [ type_ "text", readonly True, class "form-control-plaintext", value model.uploadedAt ] []
                        ]
                    ]

              else
                div [] []
            , if model.content /= "" then
                div [ class "form-group row" ]
                    [ label [ for "content", class "col-sm-2 col-form-label" ] [ text "Content" ]
                    , div [ class "col-sm-10" ]
                        [ input [ type_ "text", readonly True, class "form-control-plaintext", value model.content ] []
                        ]
                    ]

              else
                div [] []
            , if model.editable then
                div [ class "form-group row" ]
                    [ label [ for "file", class "col-sm-2 col-form-label" ]
                        [ text "File" ]
                    , div [ class "col-sm-10" ]
                        [ input
                            [ id "file"
                            , name "file"
                            , type_ "file"
                            , class "form-control-file"
                            , placeholder "File"
                            ]
                            []
                        ]
                    ]

              else
                div [] []
            , if model.editable then
                button [ type_ "submit", class "btn btn-primary" ]
                    [ text "Submit" ]

              else
                div [] []
            ]
        ]



-- JSON ENCODE/DECODE


encode : Model -> E.Value
encode model =
    E.object
        [ ( "fileName", E.string model.fileName )
        , ( "content", E.string model.content )
        , ( "filePath", E.string model.filePath )
        , ( "editable", E.bool model.editable )
        , ( "uploadedBy", E.string model.uploadedBy )
        , ( "uploadedAt", E.string model.uploadedAt )
        ]


decoder : D.Decoder Model
decoder =
    D.map6 Model
        (D.field "fileName" D.string)
        (D.field "content" D.string)
        (D.field "filePath" D.string)
        (D.field "editable" D.bool)
        (D.field "uploadedBy" D.string)
        (D.field "uploadedAt" D.string)
