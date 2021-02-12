// This is the old ItemPhonetic 
//      for BreakdownView, CharacterDisplay, etc.
// New "ItemGif.js" is in ItemDisplay/WordDisplay
//      for WordDisplay only

import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';

const Container = styled.div`
    display: inline-block;
    width: auto;
`;

const Phonetic = styled.span`
    text-align: center;
    font-size: 1.5em;
    font-weight: 200;
    white-space: nowrap;
`;

const SpeakButton = styled.i`
    position: relative;
    margin-left: 5px;
    font-weight: 200;
    cursor: pointer;
`;

const WordContainer = styled.h1`
    font-size: 3.75em;
    font-weight: 200;
    text-align: center;
`;

/**
 * Renders the Chinese, phonetic(pinyin), and an audio button.
 */
export default function ItemPhonetic(props) {

    const audio = new Audio(props.audioURL);
    // Add slashes at the beginning and the end
    const pinyin = `/${props.pinyin}/`;

    return (
        <Container>
            <Phonetic className='use-chinese'>
                { pinyin }
                <SpeakButton
                    className='fas fa-volume'
                    onClick={ audio.play }
                />
            </Phonetic>
            <WordContainer className='use-chinese'>
                {props.item}
            </WordContainer>
        </Container>
    );
}

ItemPhonetic.propTypes = {
    /** An array of possible pronunciation. */
    pinyin: PropTypes.string,
    /** The URL of the corresponding audio file. */
    audioURL: PropTypes.string.isRequired,
    /** The character to be displayed.  */
    item: PropTypes.string.isRequired
};