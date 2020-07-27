module Main exposing (..)

import Browser
import File exposing (File)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
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
    , uploadStatus : UploadStatus
    }


type UploadStatus
    = Waiting
    | Uploading Float
    | Done
    | Fail



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
            { fileName = model.fileName, content = model.content, filePath = model.filePath, editable = model.editable, uploadedBy = model.uploadedBy, uploadedAt = model.uploadedAt, uploadStatus = Waiting }

        Err _ ->
            { fileName = "", content = "", filePath = "", editable = False, uploadedBy = "", uploadedAt = "", uploadStatus = Waiting }
    , Cmd.none
    )



-- UPDATE


type Msg
    = FileNameChanged String
    | GotFiles (List File)
    | GotProgress Http.Progress
    | Uploaded (Result Http.Error ())
    | Cancel


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        FileNameChanged fileName ->
            ( { model | fileName = fileName }
            , Cmd.none
            )

        GotFiles files ->
            ( { model | uploadStatus = Uploading 0 }
            , Http.request
                { method = "POST"
                , url = "/"
                , headers = []
                , body = Http.multipartBody (List.map (Http.filePart "files[]") files)
                , expect = Http.expectWhatever Uploaded
                , timeout = Nothing
                , tracker = Just "upload"
                }
            )

        GotProgress progress ->
            case progress of
                Http.Sending p ->
                    ( { model | uploadStatus = Uploading (Http.fractionSent p) }, Cmd.none )

                Http.Receiving _ ->
                    ( model, Cmd.none )

        Uploaded result ->
            case result of
                Ok _ ->
                    ( { model | uploadStatus = Done }, Cmd.none )

                Err _ ->
                    ( { model | uploadStatus = Fail }, Cmd.none )

        Cancel ->
            ( { model | uploadStatus = Waiting }, Http.cancel "upload" )



-- VIEW


view : Model -> Html Msg
view model =
    div []
        [ case model.uploadStatus of
            Waiting ->
                input
                    [ type_ "file"
                    , multiple True
                    , on "change" (D.map GotFiles filesDecoder)
                    ]
                    []

            Uploading fraction ->
                div []
                    [ progress
                        [ value (String.fromInt (round (100 * fraction)))
                        , Html.Attributes.max "100"
                        , style "display" "block"
                        ]
                        []
                    , button [ onClick Cancel ] [ text "Cancel" ]
                    ]

            Done ->
                h1 [] [ text "DONE" ]

            Fail ->
                h1 [] [ text "FAIL" ]
        , Html.form
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



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Http.track "upload" GotProgress



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


type alias AlmostModel =
    { fileName : String
    , content : String
    , filePath : String
    , editable : Bool
    , uploadedBy : String
    , uploadedAt : String
    }


decoder : D.Decoder AlmostModel
decoder =
    D.map6 AlmostModel
        (D.field "fileName" D.string)
        (D.field "content" D.string)
        (D.field "filePath" D.string)
        (D.field "editable" D.bool)
        (D.field "uploadedBy" D.string)
        (D.field "uploadedAt" D.string)


filesDecoder : D.Decoder (List File)
filesDecoder =
    D.at [ "target", "files" ] (D.list File.decoder)
